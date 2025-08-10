# Easy RAG

## Conteúdo

 - [](#)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="create-core"></div>

## `Criando o projeto (django) core`

De início vamos criar o `core` do nosso projeto:

```bash
django-admin startproject core .
```

Agora é só executar:

```bash
python manage.py runserver
```




















---

### 1. Configuração do Projeto

- Criar ambiente virtual e instalar dependências iniciais (FastAPI ou Django, TailwindCSS, PostgreSQL client, etc.).
- Configurar conexão com o banco PostgreSQL.
- Criar estrutura inicial do projeto (pasta backend, frontend, etc.).
- Configurar variáveis de ambiente (env para chaves, URLs, etc.).
- Testar se o servidor sobe corretamente.

### 2. Sistema de Autenticação — Parte 1 (E-mail + Código)
- Implementar API para cadastro com e-mail.
- Criar endpoint para enviar código de verificação (simulado primeiro, depois com envio real via SMTP ou serviço como SendGrid).
- Endpoint para confirmar código e criar conta.
- Testes de criação de conta.

### 3. Sistema de Autenticação — Parte 2 (OAuth)
- Implementar login/registro via Google.
- Implementar login/registro via GitHub.
- Unificar login via e-mail e OAuth no mesmo fluxo.
- Testar login e logout.

### 4. Tela de Login e Registro (Frontend)
- Criar páginas separadas para Registro e Login.
- Conectar com APIs criadas.
- Validação de formulários.
- Testes no navegador.

### 5. Tela Home (Chat + Histórico de Prompts)
- Criar layout com Tailwind (prompt central + barra lateral).
- Implementar API para salvar e recuperar histórico de prompts por usuário.
- Testar inserção e listagem no frontend.

### 6. Módulo “Files” — Parte 1 (Estrutura e Upload)
- Criar página “Files” com botão na barra lateral.
- Criar API para criar pastas no banco.
- Criar API para upload de arquivos para o PostgreSQL.
- Testar uploads pequenos e grandes.

### 7. Módulo “Files” — Parte 2 (Listagem e Gerenciamento)
- Listar pastas e arquivos no frontend.
- Implementar exclusão de arquivos e pastas.
- Testes de CRUD completo.

### 8. Integração RAG com LangChain — Parte 1 (Ingestão de Dados)
- Criar pipeline para extrair texto de arquivos enviados.
- Armazenar embeddings em um banco vetorial (pode ser pgvector no PostgreSQL).
- Testar consultas simples com base nos arquivos.

### 9. Integração RAG com LangChain — Parte 2 (Chat Inteligente)
- Integrar prompt da Home com LangChain para responder usando dados do usuário.
- Melhorar contexto e precisão.
- Testar com diferentes tipos de arquivos.

### 10. Melhorias e Testes Finais
- Implementar autenticação JWT ou sessão segura.
- Revisar segurança de uploads.
- Otimizar consultas no banco.
- Testes de carga e performance.
- Ajustar responsividade no Tailwind.
