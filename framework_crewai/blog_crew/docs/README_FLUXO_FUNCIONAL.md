# Fluxo Funcional do Blog CrewAI

## Scripts Principais

### 1. Pipeline Completo
```bash
# Executar o pipeline completo (RSS → Tradução → Formatação → Imagem → Publicação)
python main.py

# Ou com limite de artigos
python run_crew.py --limit 3
```

### 2. Processamento de Imagens
```bash
# Gerar imagens para posts formatados
python process_images_working.py
```

### 3. Publicação no Sanity
```bash
# Publicar posts SEM tags/categorias/autor (evita erros)
python publish_simple.py

# Publicação tradicional (requer tags/categorias configuradas)
python publish_to_sanity.py
```

### 4. Monitor RSS
```bash
# Iniciar monitor de RSS em background
./start_monitor.sh

# Executar monitor diretamente
python rss_monitor.py
```

### 5. Sincronização com Algolia
```bash
# Sincronizar últimos 10 artigos
python sync_last_10_articles.py

# Sincronização completa
python sync_sanity_to_algolia.py
```

## Fluxo de Trabalho Recomendado

1. **Gerar novos posts**:
   ```bash
   python run_crew.py --limit 5
   ```

2. **Processar imagens**:
   ```bash
   python process_images_working.py
   ```

3. **Publicar no Sanity**:
   ```bash
   python publish_simple.py
   ```

4. **Sincronizar com Algolia** (para busca):
   ```bash
   python sync_last_10_articles.py
   ```

## Estrutura de Diretórios

```
posts_para_traduzir/   # Artigos coletados do RSS
posts_traduzidos/      # Artigos traduzidos
posts_formatados/      # Artigos formatados para Sanity
posts_com_imagem/      # Artigos com imagens geradas
posts_publicados/      # Artigos publicados no Sanity
posts_imagens/         # Backup das imagens geradas
```

## Configurações Necessárias

### Variáveis de Ambiente (.env)
```
OPENAI_API_KEY=sk-...          # Para DALL-E 3
GOOGLE_API_KEY=...             # Para Gemini (tradução)
SANITY_PROJECT_ID=brby2yrg
SANITY_DATASET=production
SANITY_API_TOKEN=sk...
ALGOLIA_APP_ID=...
ALGOLIA_API_KEY=...
```

## Scripts Utilitários

- `delete_sanity_duplicates.py` - Remove posts duplicados no Sanity
- `delete_algolia_duplicates.py` - Remove duplicados no Algolia
- `list_sanity_documents.py` - Lista documentos no Sanity
- `edit_post.py` - Edita um post específico
- `view_post.py` - Visualiza um post

## Notas Importantes

1. **Tags**: O script `publish_simple.py` remove automaticamente tags/categorias/autor para evitar erros de validação no Sanity.

2. **Imagens**: Todas as imagens são geradas com DALL-E 3 e fazem upload binário direto para o Sanity.

3. **Processamento**: O sistema usa Gemini para tradução/formatação e OpenAI para geração de imagens.