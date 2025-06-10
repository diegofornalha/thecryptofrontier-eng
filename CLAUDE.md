# CLAUDE.md - Diretrizes de Organização do Projeto

## 📁 Estrutura de Diretórios

Este projeto segue uma organização específica para manter os arquivos bem estruturados. **SEMPRE** siga estas diretrizes ao criar novos arquivos:

### 🏗️ Estrutura Principal

```
/Users/agents/thecryptofrontier/
├── docs/                    # Toda documentação do projeto
├── scripts/                 # Scripts utilitários
│   ├── docker/             # Scripts relacionados ao Docker
│   └── patches/            # Scripts de patches e workarounds
├── framework_crewai/        # Framework CrewAI para automação de blog
├── src/                     # Código fonte principal do Next.js
├── public/                  # Assets públicos
└── [arquivos de config]     # package.json, docker-compose.yml, etc (raiz)
```

### 📝 Onde Colocar Cada Tipo de Arquivo

#### Documentação
**Localização:** `/docs/`
- Arquivos `.md` de documentação
- Instruções de deploy
- Guias de configuração
- Documentação técnica

#### Scripts Docker
**Localização:** `/scripts/docker/`
- Scripts de inicialização (`docker-start.sh`)
- Scripts de monitoramento (`monitor-container.sh`)
- Scripts de produção (`start-production.sh`, `update-production.sh`)
- Scripts de deploy (`deploy-studio.sh`)

#### Scripts de Patches
**Localização:** `/scripts/patches/`
- Workarounds (`sanity-workaround.js`)
- Patches de dependências (`patch-nanoid.js`)
- Scripts de correção (`apply-preload-patch.js`)

#### Scripts Gerais
**Localização:** `/scripts/`
- Geradores de código (`generate_python_schemas.ts`)
- Scripts de migração
- Utilitários diversos

#### Framework CrewAI
**Localização:** `/framework_crewai/blog_crew/`
- Scripts Python para automação
- Ferramentas de sincronização
- Agentes e tarefas

### ⚠️ Arquivos que DEVEM Permanecer na Raiz

Estes arquivos são padrão e devem ficar na raiz:
- `package.json`
- `docker-compose.yml`
- `docker-compose.production.yml`
- `Dockerfile.nextjs`
- `next.config.js`
- `tailwind.config.js`
- `tsconfig.json`
- `postcss.config.js`
- `.env` files
- `netlify.toml`
- `sanity.config.ts`
- `sanity.cli.ts`

### 🚫 O que NÃO Fazer

1. **Nunca** coloque scripts soltos na raiz
2. **Nunca** misture documentação com código
3. **Nunca** crie arquivos temporários na raiz
4. **Sempre** use as pastas apropriadas

### 🔄 Atualizando Referências

Quando mover arquivos, lembre-se de atualizar:
1. Scripts que referenciam os arquivos movidos
2. `package.json` scripts
3. Dockerfiles
4. Documentação

### 📋 Checklist para Novos Arquivos

Antes de criar um arquivo, pergunte-se:
- [ ] É documentação? → `/docs/`
- [ ] É um script Docker? → `/scripts/docker/`
- [ ] É um patch/workaround? → `/scripts/patches/`
- [ ] É um script utilitário? → `/scripts/`
- [ ] É parte do CrewAI? → `/framework_crewai/blog_crew/`
- [ ] É código do Next.js? → `/src/`
- [ ] É um arquivo de configuração padrão? → Raiz

### 💡 Exemplos Práticos

```bash
# ❌ Errado
/Users/agents/thecryptofrontier/deploy-instructions.md
/Users/agents/thecryptofrontier/fix-sanity.js

# ✅ Correto
/Users/agents/thecryptofrontier/docs/deploy-instructions.md
/Users/agents/thecryptofrontier/scripts/patches/fix-sanity.js
```

---

Este arquivo deve ser consultado sempre que for criar novos arquivos no projeto.