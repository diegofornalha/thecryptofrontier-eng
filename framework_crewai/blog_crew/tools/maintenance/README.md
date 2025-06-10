# 🛠️ Scripts de Manutenção

Esta pasta contém scripts utilitários para manutenção manual do sistema de blog.

## 📋 Scripts Disponíveis

### Gestão de Posts

#### `delete_by_title.py`
Remove posts do Sanity por título específico.
```bash
python delete_by_title.py "Título do Post"
```

#### `edit_post.py`
Edita posts existentes no Sanity CMS.
```bash
python edit_post.py
```

#### `list_sanity_documents.py`
Lista todos os documentos no Sanity para verificação.
```bash
python list_sanity_documents.py
```

### Sincronização

#### `sync_last_10_articles.py`
Sincroniza apenas os últimos 10 artigos do Sanity para o Algolia.
Útil para testes rápidos sem sincronizar toda a base.
```bash
python sync_last_10_articles.py
```

### Limpeza U.Today

#### `delete_utoday_posts.py`
Remove posts do U.Today do Sanity CMS.
```bash
python delete_utoday_posts.py
```

#### `delete_utoday_algolia.py`
Remove posts do U.Today do índice Algolia.
```bash
python delete_utoday_algolia.py
```

## ⚠️ Cuidados

- Sempre faça backup antes de executar scripts de deleção
- Use o modo `--dry-run` quando disponível para simular
- Verifique as variáveis de ambiente necessárias:
  - `SANITY_API_TOKEN`
  - `SANITY_PROJECT_ID`
  - `ALGOLIA_APP_ID`
  - `ALGOLIA_ADMIN_API_KEY`

## 🔧 Quando Usar

- **Correções pontuais**: Editar ou remover posts específicos
- **Debug**: Listar documentos para investigar problemas
- **Testes**: Sincronizar pequenos batches para testar mudanças
- **Limpeza**: Remover conteúdo indesejado de fontes específicas