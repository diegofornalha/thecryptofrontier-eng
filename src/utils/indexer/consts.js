const ALGOLIA_APP_ID = process.env.NEXT_PUBLIC_ALGOLIA_APP_ID || '';
const ALGOLIA_INDEX_NAME_SUFFIX = process.env.NEXT_PUBLIC_ALGOLIA_INDEX_NAME || 'mcpx_content';
const ALGOLIA_SEARCH_API_KEY = process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY || '';

const ALGOLIA_ADMIN_API_KEY = process.env.ALGOLIA_ADMIN_API_KEY || '';
// Definir o nome do ambiente para indexação
const ENV_NAME = process.env.NODE_ENV || 'development';

function buildIndexName() {
    // Conforme especificado na documentação, sempre usar o nome fixo "development_mcpx_content"
    return 'development_mcpx_content';
    
    // Código anterior comentado abaixo:
    /*
    if (!ALGOLIA_INDEX_NAME_SUFFIX) {
        return null;
    }
    
    // Verificar se o SUFFIX já inclui o prefixo do ambiente para evitar duplicação
    if (ALGOLIA_INDEX_NAME_SUFFIX.startsWith(ENV_NAME + '_')) {
        return ALGOLIA_INDEX_NAME_SUFFIX;
    }
    
    const indexName = ENV_NAME + '_' + ALGOLIA_INDEX_NAME_SUFFIX;
    return indexName;
    */
}

module.exports = {
    ALGOLIA_APP_ID,
    ALGOLIA_INDEX_NAME_SUFFIX,
    ALGOLIA_SEARCH_API_KEY,
    ALGOLIA_ADMIN_API_KEY,
    ENV_NAME,
    buildIndexName
};
