describe('Chat Interface E2E Tests', () => {
  beforeEach(() => {
    const mockAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mockTokenForTesting';
    const mockDBCredentials = {
      dbType: 'postgres',
      user: 'testuser',
      password: 'testpass',
      host: 'localhost',
      port: 5432,
      db_name: 'testdb',
      schema_name: 'public'
    };

    cy.window().then((win) => {
      win.sessionStorage.setItem('access_token', mockAccessToken);
      win.sessionStorage.setItem('dbCredentials', JSON.stringify(mockDBCredentials));
    });

    cy.intercept('POST', '**/text-to-sql/chat', (req) => {
      if (req.body?.user_input?.toLowerCase().includes('error')) {
        req.reply({
          statusCode: 500,
          body: { error: true, message: 'Simulated error' }
        });
      } else {
        req.reply({
          statusCode: 200,
          body: {
            data: {
              results: {
                header: 'Here are the **results** for your query.',
                sql_results: "[{'id': 1, 'name': 'Sample Data', 'value': 100}]"
              }
            }
          }
        });
      }
    }).as('queryRequest');

    cy.intercept('POST', '**/text-to-sql/chat', (req) => {
      expect(req.headers['authorization']).to.exist;
      expect(req.headers['authorization']).to.include(mockAccessToken);
    });

    cy.visit('/query');
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
    cy.get('.chat-message.user-message').should('be.visible').contains(userMessage);
  });

  it('should handle error responses', () => {
    const errorMessage = 'This will cause an error';
    cy.get('.chat-input').type(errorMessage).type('{enter}');
    cy.get('.chat-message.user-message').should('be.visible').contains(errorMessage);
    cy.wait('@queryRequest');
    cy.get('.chat-message.bot-message').should('be.visible').contains('Error processing your query');
  });

  it('should clear input field after sending message', () => {
    const userMessage = 'Show me sales data';
    cy.get('.chat-input').type(userMessage);
    cy.get('.chat-input').should('have.value', userMessage);
    cy.get('.chat-input').type('{enter}');
    cy.get('.chat-message.user-message').should('be.visible');
    cy.get('.chat-input').should('have.value', '');
  });

  it('should send message when clicking the send button', () => {
    const userMessage = 'Show me customer data';
    cy.get('.chat-input').type(userMessage);
    cy.get('.btn-custom-send').click();
    cy.get('.chat-message.user-message').should('be.visible').contains(userMessage);
  });

  it('should correctly display multiple messages in sequence', () => {
    cy.get('.chat-input').type('First query').type('{enter}');
    cy.get('.chat-message.user-message').should('be.visible').contains('First query');
    cy.wait('@queryRequest');
    cy.get('.chat-input').type('Second query').type('{enter}');
    cy.wait('@queryRequest');
    cy.get('.chat-message.user-message').eq(0).contains('First query');
    cy.get('.chat-message.user-message').eq(1).contains('Second query');
  });
});
