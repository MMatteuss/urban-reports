# Urban Reports

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Um sistema web colaborativo para reportar problemas urbanos em sua cidade. Permite que cidadãos reportem problemas como buracos, esgotos abertos, lixo acumulado, postes caídos e outros, acompanhando o status das solicitações.

## 🚀 Funcionalidades

### 👤 Gestão de Usuários
- Registro com validação de dados
- Login com "Lembrar-me"
- Perfil personalizável com foto
- Modo claro/escuro
- Controle de notificações

### 📋 Sistema de Reportes
- Criação de reportes com fotos
- Categorização de problemas
- Geolocalização com mapa interativo
- Status dos reportes (pendente, em andamento, resolvido)
- Busca por localização e categoria

### 💬 Interação Social
- Comentários nos reportes
- Sistema de votação (upvote/downvote)
- Compartilhamento de reportes
- Dashboard pessoal

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM para banco de dados
- **Flask-Login** - Gestão de autenticação
- **SQLite** - Banco de dados (pode ser trocado por PostgreSQL)

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização
- **Bootstrap 5** - Framework CSS responsivo
- **JavaScript** - Interatividade
- **Leaflet.js** - Mapas interativos

### Outras Bibliotecas
- **Werkzeug** - Segurança e upload de arquivos
- **Pillow** - Processamento de imagens
- **python-dotenv** - Gestão de variáveis de ambiente

## 📁 Estrutura do Projeto

```
urban-reports/
│
├── app.py                    # Aplicação principal Flask
├── requirements.txt          # Dependências do projeto
├── .env                      # Variáveis de ambiente
├── .gitignore               # Arquivos ignorados pelo Git
│
├── static/                   # Arquivos estáticos
│   ├── css/
│   │   └── style.css        # Estilos personalizados
│   ├── js/
│   │   └── script.js        # JavaScript customizado
│   └── uploads/             # Imagens enviadas pelos usuários
│       ├── profiles/        # Fotos de perfil
│       └── reports/         # Fotos dos reportes
│
├── templates/                # Templates HTML
│   ├── base.html            # Template base
│   ├── index.html           # Página inicial
│   ├── login.html           # Página de login
│   ├── register.html        # Página de registro
│   ├── dashboard.html       # Dashboard do usuário
│   ├── profile.html         # Perfil do usuário
│   ├── new_report.html      # Formulário de novo reporte
│   ├── search.html          # Busca
│   ├── report_detail.html   # Detalhes do reporte
│   └── edit_profile.html    # Edição de perfil
│
└── database/                # Diretório do banco de dados
    └── urban_reports.db     # Arquivo do banco SQLite
```

## ⚙️ Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional)

### Passos de Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/urban-reports.git
cd urban-reports
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# No Windows
venv\Scripts\activate

# No Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
# Crie um arquivo .env na raiz do projeto
# Copie o conteúdo abaixo e ajuste conforme necessário

SECRET_KEY=sua-chave-secreta-aqui-123456
DATABASE_URL=sqlite:///database/urban_reports.db
```

5. **Inicialize o banco de dados**
```bash
# Execute o aplicativo pela primeira vez
python app.py

# Ou se preferir, execute:
python -c "from app import db, app; with app.app_context(): db.create_all()"
```

6. **Execute o servidor de desenvolvimento**
```bash
python app.py
```

7. **Acesse a aplicação**
Abra seu navegador e acesse: `http://localhost:5000`

## 🧪 Testando a Aplicação

### Usuário de Teste
Ao iniciar pela primeira vez, um usuário de teste é criado automaticamente:
- **Email:** test@test.com
- **Senha:** test123

### Criando um Novo Usuário
1. Acesse `http://localhost:5000/register`
2. Preencha o formulário de registro
3. Faça login com suas credenciais

### Criando um Reporte
1. Faça login na aplicação
2. Clique em "Novo Reporte" no menu
3. Preencha os detalhes do problema
4. Adicione fotos (opcional)
5. Clique em "Publicar Reporte"

## 🐛 Solução de Problemas Comuns

### Erro: "unable to open database file"
**Solução:** Certifique-se de que o diretório `database/` existe e tem permissões de escrita.

### Erro: "jinja2.exceptions.UndefinedError"
**Solução:** Verifique se todos os templates estão na pasta `templates/` e se as variáveis passadas estão corretas.

### Erro: "No module named 'flask'"
**Solução:** Ative o ambiente virtual e instale as dependências novamente:
```bash
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### Upload de Imagens não funciona
**Solução:** Verifique se a pasta `static/uploads/` existe e tem permissões de escrita.

## 📊 API Endpoints

A aplicação também oferece uma API REST básica:

- `GET /api/reports` - Lista os últimos 50 reportes
- `POST /report/<id>/comment` - Adiciona um comentário
- `POST /report/<id>/vote` - Vota em um reporte
- `POST /toggle-dark-mode` - Alterna modo claro/escuro
- `POST /toggle-notifications` - Alterna notificações

## 🔒 Segurança

- Senhas hashadas com bcrypt
- Proteção contra CSRF
- Validação de arquivos uploadados
- Sanitização de inputs
- Sessões seguras

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:
- Desktop
- Tablets
- Smartphones

## 🚀 Implantação em Produção

Para implantar em produção, recomendamos:

1. **Use um servidor WSGI:** Gunicorn ou uWSGI
2. **Use um servidor web:** Nginx ou Apache
3. **Configure um banco de dados mais robusto:** PostgreSQL
4. **Use variáveis de ambiente reais**
5. **Configure HTTPS/SSL**
6. **Habilite logging apropriado**

### Exemplo com Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🤝 Como Contribuir

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

Para suporte, entre em contato:
- **Email:** suporte@urbanreports.com
- **Issues:** [GitHub Issues](https://github.com/seu-usuario/urban-reports/issues)

## ✨ Melhorias Futuras

- [ ] App mobile (React Native/Flutter)
- [ ] Sistema de notificações por email
- [ ] Painel administrativo
- [ ] Relatórios PDF
- [ ] Integração com redes sociais
- [ ] Sistema de ranking de usuários
- [ ] Machine Learning para classificação automática

## 👥 Autores

- **Mateus Monteiro** - [@mateusmonteiro](https://github.com/mateusmonteiro)
- **Contribuidores** - [ninguem]()

## 🙏 Agradecimentos

- Equipe de desenvolvimento
- Comunidade open source
- Todos os usuários que contribuem com reportes

---