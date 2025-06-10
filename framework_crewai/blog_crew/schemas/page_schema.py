# -*- coding: utf-8 -*-
# Gerado automaticamente a partir de src/sanity/schemaTypes/documents/page.ts
# NÃO EDITE MANUALMENTE - Altere o schema TS e regenere.

schema = {
    'name': 'page',
    'title': 'Página',
    'type': 'document',
    'fields': [
        {
        'name': 'title',
        'title': 'Título',
        'type': 'string',
        'validation': 'Rule => Rule.required()'
    },
        {
        'name': 'slug',
        'title': 'Slug',
        'type': 'slug',
        'options': {
            'source': 'title',
            'maxLength': '96'
        },
        'validation': 'Rule => Rule.required()'
    },
        {
        'name': 'mainImage',
        'title': 'Imagem Principal',
        'type': 'mainImage'
    },
        {
        'name': 'excerpt',
        'title': 'Resumo',
        'type': 'text',
        'rows': '3'
    },
        {
        'name': 'content',
        'title': 'Conteúdo',
        'type': 'array',
        'of': [
            {
            'type': 'block',
            'styles': [
                {
                'title': 'Normal',
                'value': 'normal'
            },
                {
                'title': 'H1',
                'value': 'h1'
            },
                {
                'title': 'H2',
                'value': 'h2'
            },
                {
                'title': 'H3',
                'value': 'h3'
            },
                {
                'title': 'H4',
                'value': 'h4'
            },
                {
                'title': 'Quote',
                'value': 'blockquote'
            }
            ]
        },
            {
            'type': 'image',
            'options': {
                'hotspot': 'true'
            },
            'fields': [
                {
                'name': 'caption',
                'type': 'string',
                'title': 'Legenda'
            },
                {
                'name': 'alt',
                'type': 'string',
                'title': 'Texto Alternativo'
            }
            ]
        },
            {
            'type': 'code'
        }
        ],
        'validation': 'Rule => Rule.required()'
    },
        {
        'name': 'seo',
        'title': 'SEO & Social',
        'type': 'seo'
    }
    ],
    'preview': {
        'select': {
            'title': 'title',
            'media': 'mainImage'
        }
    }
}
