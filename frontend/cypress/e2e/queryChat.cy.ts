describe('Chat Interface E2E Tests', () => {
    beforeEach(() => {
        cy.visit('/query');
        
        cy.intercept('POST', '**/api/text-to-sql/proccess_query', (req) => {
            if (req.body?.query?.toLowerCase().includes('error')) {
                req.reply({
                    statusCode: 500,
                    body: { error: 'Simulated error' }
                });
            } else {
                req.reply({
                    statusCode: 200,
                    body: {
                        header: 'Here are the **results** for your query.',
                        sql_results: "[{'id': 1, 'name': 'Sample Data', 'value': 100}]"
                    }
                });
            }
        }).as('queryRequest');
    });

    it('should load the chat interface', () => {
        cy.get('.chat-container').should('be.visible');
        cy.get('.chat-input').should('be.visible');
        cy.get('.btn-custom-send').should('be.visible');
    });

    it('should not send empty messages', () => {
        cy.get('.chat-input').type(' ').type('{enter}');
        cy.get('.chat-message').should('not.exist');
    });

    it('should send a message and display user message', () => {
        const userMessage = 'Show me sales data';
        cy.get('.chat-input').type(userMessage).type('{enter}');
        cy.get('.user-message').should('contain', userMessage);
    });

    it('should handle error responses', () => {
        cy.get('.chat-input').type('This will cause an error').type('{enter}');
        cy.wait('@queryRequest');
        cy.get('.bot-message').should('contain', 'Error processing your query');
    });

    it('should clear input field after sending message', () => {
        cy.get('.chat-input').type('Show me sales data').type('{enter}');
        cy.get('.chat-input').should('have.value', '');
    });

    it('should send message when clicking the send button', () => {
        const userMessage = 'Show me customer data';
        cy.get('.chat-input').type(userMessage);
        cy.get('.btn-custom-send').click();
        cy.get('.user-message').should('contain', userMessage);
    });

    it('should correctly display multiple messages in sequence', () => {
        cy.get('.chat-input').type('First query').type('{enter}');
        cy.wait('@querRequest');
        cy.get('.chat-input').type('Second query').type('{enter}');
        cy.wait('@queryRequest');
        cy.get('.user-message').eq(0).should('contain', 'First query');
        cy.get('.user-message').eq(1).should('contain', 'Second query');
    });
});