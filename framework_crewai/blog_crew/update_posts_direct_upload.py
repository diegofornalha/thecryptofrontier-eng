#!/usr/bin/env python3
"""
Script para atualizar posts existentes no Sanity com suas imagens geradas
Usa upload direto de imagem como no teste bem-sucedido
"""

import os
import json
import logging
import requests
from pathlib import Path
from datetime import datetime
import re
import unicodedata
from dotenv import load_dotenv
from PIL import Image
import io
import time

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("update_posts_images")

# Sanity config
SANITY_PROJECT_ID = os.environ.get("SANITY_PROJECT_ID", "brby2yrg")
SANITY_DATASET = "production"
SANITY_API_TOKEN = os.environ.get("SANITY_API_TOKEN")
SANITY_API_VERSION = "2021-03-25"  # Usando a versão do teste bem-sucedido

# Diretórios
IMAGES_DIR = Path("posts_imagens")
PUBLISHED_DIR = Path("posts_publicados")

def get_api_url(endpoint="query"):
    """Retorna URL da API do Sanity"""
    if endpoint == "query":
        return f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/query/{SANITY_DATASET}"
    else:
        return f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/mutate/{SANITY_DATASET}"

def get_headers():
    """Retorna headers para requisição"""
    headers = {"Content-Type": "application/json"}
    if SANITY_API_TOKEN:
        headers["Authorization"] = f"Bearer {SANITY_API_TOKEN}"
    return headers

def create_slug(title: str) -> str:
    """Cria slug a partir do título"""
    # Normalizar para remover acentos
    slug = unicodedata.normalize('NFKD', title.lower())
    slug = slug.encode('ascii', 'ignore').decode('ascii')
    # Remover caracteres especiais
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug[:80]

def list_recent_posts(limit=20):
    """Lista posts recentes do Sanity"""
    query = f'*[_type == "post"] | order(publishedAt desc)[0..{limit-1}]{{_id, title, slug, mainImage, publishedAt}}'
    url = f"{get_api_url('query')}?query={query}"
    
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json().get("result", [])
    else:
        logger.error(f"Erro ao buscar posts: {response.status_code}")
        return []

def compress_image(image_path: Path, max_size_mb: float = 1.5) -> bytes:
    """Comprime uma imagem para reduzir o tamanho"""
    try:
        # Abrir imagem
        img = Image.open(image_path)
        
        # Converter para RGB se necessário
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode not in ('RGB',):
            img = img.convert('RGB')
        
        # Redimensionar se muito grande
        max_dimension = 1600
        if img.width > max_dimension or img.height > max_dimension:
            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            logger.info(f"Imagem redimensionada para: {img.size}")
        
        # Salvar como PNG otimizado
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        size_mb = buffer.tell() / (1024 * 1024)
        logger.info(f"Imagem preparada: {size_mb:.2f}MB")
        
        buffer.seek(0)
        return buffer.read()
        
    except Exception as e:
        logger.error(f"Erro ao processar imagem: {e}")
        return None

def upload_image_to_sanity_direct(image_path: Path) -> str:
    """Upload direto de imagem para o Sanity (como no teste bem-sucedido)"""
    try:
        # Ler e processar imagem
        image_data = compress_image(image_path)
        if not image_data:
            # Tentar ler diretamente se falhar compressão
            with open(image_path, 'rb') as f:
                image_data = f.read()
        
        # URL de upload
        upload_url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/assets/images/{SANITY_DATASET}"
        
        # Headers como no teste bem-sucedido
        headers = {
            "Authorization": f"Bearer {SANITY_API_TOKEN}",
            "Content-Type": "image/png"
        }
        
        # Fazer upload direto com dados da imagem
        filename = f"crypto-{int(time.time())}.png"
        response = requests.post(
            upload_url,
            headers=headers,
            data=image_data,
            params={"filename": filename}
        )
        
        if response.status_code == 200:
            result = response.json()
            asset_id = result["document"]["_id"]
            logger.info(f"✅ Imagem enviada com sucesso!")
            logger.info(f"   Asset ID: {asset_id}")
            return asset_id
        else:
            logger.error(f"❌ Erro no upload: {response.status_code}")
            logger.error(f"   Resposta: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Erro ao fazer upload: {e}")
        import traceback
        traceback.print_exc()
        return None

def update_post_with_image(post_id: str, image_asset_id: str) -> bool:
    """Atualiza um post existente com uma imagem"""
    try:
        mutations = {
            "mutations": [{
                "patch": {
                    "id": post_id,
                    "set": {
                        "mainImage": {
                            "_type": "image",
                            "asset": {
                                "_type": "reference",
                                "_ref": image_asset_id
                            },
                            "alt": "Imagem do artigo sobre criptomoedas"
                        }
                    }
                }
            }]
        }
        
        response = requests.post(
            get_api_url('mutate'), 
            headers=get_headers(), 
            json=mutations
        )
        
        if response.status_code == 200:
            logger.info(f"✅ Post {post_id} atualizado com imagem!")
            return True
        else:
            logger.error(f"❌ Erro ao atualizar post: {response.status_code}")
            logger.error(response.text)
            return False
            
    except Exception as e:
        logger.error(f"Erro ao atualizar post: {e}")
        return False

def find_matching_image(title: str, timestamp: str = None) -> Path:
    """Tenta encontrar uma imagem correspondente ao post"""
    # Lista todas as imagens disponíveis
    images = sorted(IMAGES_DIR.glob("crypto_*.png"))
    
    if not images:
        # Tentar também com bitcoin-test
        images = sorted(IMAGES_DIR.glob("bitcoin-test-*.png"))
    
    if not images:
        return None
    
    # Se temos timestamp do arquivo publicado, tentar encontrar imagem próxima
    if timestamp:
        try:
            # Extrair timestamp do nome do arquivo
            post_timestamp = int(timestamp.split('_')[1])
            
            # Procurar imagem com timestamp próximo (dentro de 5 minutos)
            for image in images:
                match = re.search(r'crypto_(\d+)_', image.name)
                if match:
                    img_timestamp = int(match.group(1))
                    if abs(img_timestamp - post_timestamp) < 300:  # 5 minutos
                        return image
        except:
            pass
    
    # Se não encontrou por timestamp, retornar primeira imagem disponível
    return images[0] if images else None

def main():
    logger.info("""
╔══════════════════════════════════════════════════════════════╗
║    ATUALIZAÇÃO DE POSTS COM UPLOAD DIRETO DE IMAGENS        ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    if not SANITY_API_TOKEN:
        logger.error("❌ SANITY_API_TOKEN não configurado!")
        return
    
    # 1. Buscar posts recentes do Sanity
    logger.info("📋 Buscando posts recentes do Sanity...")
    posts = list_recent_posts()
    
    # Filtrar posts sem imagem
    posts_sem_imagem = [p for p in posts if not p.get('mainImage')]
    logger.info(f"Encontrados {len(posts_sem_imagem)} posts sem imagem")
    
    if not posts_sem_imagem:
        logger.info("✅ Todos os posts já têm imagem!")
        return
    
    # 2. Listar arquivos publicados
    published_files = list(PUBLISHED_DIR.glob("*.json"))
    logger.info(f"Encontrados {len(published_files)} arquivos publicados")
    
    # 3. Processar cada post sem imagem
    updated_count = 0
    
    for i, post in enumerate(posts_sem_imagem):
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Post {i+1}/{len(posts_sem_imagem)}: {post['title']}")
            post_slug = post.get('slug', {}).get('current', '')
            
            # Tentar encontrar arquivo publicado correspondente
            matching_file = None
            for pub_file in published_files:
                with open(pub_file, 'r', encoding='utf-8') as f:
                    pub_data = json.load(f)
                    pub_title_pt = pub_data.get('title_pt', '')
                    
                    # Comparar por slug ou título similar
                    if (create_slug(pub_title_pt) == post_slug or 
                        pub_title_pt.lower() in post['title'].lower() or
                        post['title'].lower() in pub_title_pt.lower()):
                        matching_file = pub_file
                        break
            
            # Encontrar imagem
            if matching_file:
                # Extrair timestamp do nome do arquivo
                timestamp = matching_file.stem
                image_path = find_matching_image(post['title'], timestamp)
            else:
                # Usar qualquer imagem disponível
                image_path = find_matching_image(post['title'])
            
            if image_path:
                logger.info(f"🎨 Usando imagem: {image_path.name}")
                
                # Upload direto da imagem
                asset_id = upload_image_to_sanity_direct(image_path)
                
                if asset_id:
                    # Atualizar post
                    if update_post_with_image(post['_id'], asset_id):
                        updated_count += 1
                        # Mover imagem para pasta de processadas
                        processed_dir = Path("posts_imagens_usadas")
                        processed_dir.mkdir(exist_ok=True)
                        image_path.rename(processed_dir / image_path.name)
                        logger.info(f"✅ Imagem movida para: {processed_dir}")
            else:
                logger.warning(f"⚠️  Nenhuma imagem disponível para este post")
                
        except Exception as e:
            logger.error(f"Erro ao processar post: {e}")
            import traceback
            traceback.print_exc()
    
    # Resumo
    logger.info(f"""
╔══════════════════════════════════════════════════════════════╗
║                        CONCLUÍDO                             ║
║                                                              ║
║   Posts atualizados com imagem: {updated_count}/{len(posts_sem_imagem)}                       ║
╚══════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()