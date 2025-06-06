# Consultas SQL para Análise dos Dados

## Análises Básicas

### 1. Total de Vendas por Ano e Categoria

```sql
SELECT 
    d.ano,
    p.categoria,
    SUM(f.valor_venda) as total_vendas,
    COUNT(DISTINCT f.id_pedido) as total_pedidos
FROM 
    fato.vendas f
JOIN 
    dim.data d ON f.chave_data = d.chave_data
JOIN 
    dim.produto p ON f.chave_produto = p.chave_produto
GROUP BY 
    d.ano, p.categoria
ORDER BY 
    d.ano, total_vendas DESC;
```

### 2. Lucro por Estado e Trimestre

```sql
SELECT 
    l.estado,
    d.ano,
    d.trimestre,
    SUM(f.lucro) as lucro_total,
    SUM(f.valor_venda) as vendas_total,
    ROUND((SUM(f.lucro) / NULLIF(SUM(f.valor_venda), 0)) * 100, 2) as margem_lucro
FROM 
    fato.vendas f
JOIN 
    dim.data d ON f.chave_data = d.chave_data
JOIN 
    dim.localizacao l ON f.chave_localizacao = l.chave_localizacao
GROUP BY 
    l.estado, d.ano, d.trimestre
ORDER BY 
    d.ano, d.trimestre, lucro_total DESC;
```

### 3. Top 10 Produtos Mais Vendidos

```sql
SELECT 
    p.nome_produto,
    p.categoria,
    p.subcategoria,
    SUM(f.quantidade) as quantidade_total,
    SUM(f.valor_venda) as vendas_total
FROM 
    fato.vendas f
JOIN 
    dim.produto p ON f.chave_produto = p.chave_produto
GROUP BY 
    p.nome_produto, p.categoria, p.subcategoria
ORDER BY 
    quantidade_total DESC
LIMIT 10;
```

## Análises Intermediárias

### 4. Vendas por Dia da Semana

```sql
SELECT 
    d.nome_dia,
    SUM(f.valor_venda) as vendas_total,
    COUNT(DISTINCT f.id_pedido) as total_pedidos,
    ROUND(AVG(f.valor_venda), 2) as ticket_medio
FROM 
    fato.vendas f
JOIN 
    dim.data d ON f.chave_data = d.chave_data
GROUP BY 
    d.nome_dia
ORDER BY 
    CASE
        WHEN d.nome_dia = 'Monday' THEN 1
        WHEN d.nome_dia = 'Tuesday' THEN 2
        WHEN d.nome_dia = 'Wednesday' THEN 3
        WHEN d.nome_dia = 'Thursday' THEN 4
        WHEN d.nome_dia = 'Friday' THEN 5
        WHEN d.nome_dia = 'Saturday' THEN 6
        WHEN d.nome_dia = 'Sunday' THEN 7
    END;
```

### 5. Comparação: Dias Úteis vs. Fim de Semana

```sql
SELECT 
    CASE WHEN d.eh_fim_semana THEN 'Fim de Semana' ELSE 'Dia Útil' END as tipo_dia,
    SUM(f.valor_venda) as vendas_total,
    COUNT(DISTINCT f.id_pedido) as total_pedidos,
    COUNT(DISTINCT d.data_completa) as total_dias,
    ROUND(SUM(f.valor_venda) / COUNT(DISTINCT d.data_completa), 2) as media_vendas_por_dia
FROM 
    fato.vendas f
JOIN 
    dim.data d ON f.chave_data = d.chave_data
GROUP BY 
    d.eh_fim_semana
ORDER BY 
    d.eh_fim_semana;
```

### 6. Análise de Descontos e Lucratividade

```sql
SELECT 
    CASE 
        WHEN f.desconto = 0 THEN 'Sem Desconto'
        WHEN f.desconto <= 0.1 THEN '1-10%'
        WHEN f.desconto <= 0.2 THEN '11-20%'
        WHEN f.desconto <= 0.3 THEN '21-30%'
        WHEN f.desconto <= 0.4 THEN '31-40%'
        ELSE '> 40%'
    END as faixa_desconto,
    COUNT(*) as total_vendas,
    ROUND(AVG(f.desconto) * 100, 2) as desconto_medio,
    SUM(f.valor_venda) as vendas_total,
    SUM(f.lucro) as lucro_total,
    ROUND(SUM(f.lucro) / NULLIF(SUM(f.valor_venda), 0) * 100, 2) as margem_lucro
FROM 
    fato.vendas f
GROUP BY 
    faixa_desconto
ORDER BY 
    desconto_medio;
```

## Análises Avançadas

### 7. Análise RFV (Recência, Frequência, Valor)

```sql
WITH cliente_rfv AS (
    SELECT 
        f.chave_cliente,
        MAX(d.data_completa) as ultima_compra,
        COUNT(DISTINCT f.id_pedido) as frequencia,
        SUM(f.valor_venda) as valor_monetario
    FROM 
        fato.vendas f
    JOIN 
        dim.data d ON f.chave_data = d.chave_data
    GROUP BY 
        f.chave_cliente
),
pontuacao_rfv AS (
    SELECT 
        c.nome_cliente,
        c.segmento,
        NTILE(5) OVER (ORDER BY crfv.ultima_compra) as pontuacao_recencia,
        NTILE(5) OVER (ORDER BY crfv.frequencia) as pontuacao_frequencia,
        NTILE(5) OVER (ORDER BY crfv.valor_monetario) as pontuacao_valor
    FROM 
        cliente_rfv crfv
    JOIN 
        dim.cliente c ON crfv.chave_cliente = c.chave_cliente
)
SELECT 
    nome_cliente,
    segmento,
    pontuacao_recencia,
    pontuacao_frequencia,
    pontuacao_valor,
    pontuacao_recencia + pontuacao_frequencia + pontuacao_valor as pontuacao_rfv
FROM 
    pontuacao_rfv
ORDER BY 
    pontuacao_rfv DESC
LIMIT 20;
```

### 8. Análise de Cesta de Compras (Produtos Frequentemente Comprados Juntos)

```sql
WITH pares_produtos AS (
    SELECT 
        a.id_pedido,
        a.chave_produto as produto1,
        b.chave_produto as produto2
    FROM 
        fato.vendas a
    JOIN 
        fato.vendas b ON a.id_pedido = b.id_pedido AND a.chave_produto < b.chave_produto
)
SELECT 
    p1.nome_produto as produto1,
    p2.nome_produto as produto2,
    COUNT(*) as frequencia_conjunta
FROM 
    pares_produtos pp
JOIN 
    dim.produto p1 ON pp.produto1 = p1.chave_produto
JOIN 
    dim.produto p2 ON pp.produto2 = p2.chave_produto
GROUP BY 
    p1.nome_produto, p2.nome_produto
ORDER BY 
    frequencia_conjunta DESC
LIMIT 15;
```

### 9. Análise de Tendência Mensal por Categoria

```sql
SELECT 
    d.ano,
    d.mes,
    d.nome_mes,
    p.categoria,
    SUM(f.valor_venda) as vendas_total,
    SUM(f.lucro) as lucro_total,
    COUNT(DISTINCT f.id_pedido) as total_pedidos
FROM 
    fato.vendas f
JOIN 
    dim.data d ON f.chave_data = d.chave_data
JOIN 
    dim.produto p ON f.chave_produto = p.chave_produto
GROUP BY 
    d.ano, d.mes, d.nome_mes, p.categoria
ORDER BY 
    d.ano, d.mes, vendas_total DESC;
```

### 10. Segmentação de Clientes por Valor de Compra e Frequência

```sql
WITH metricas_cliente AS (
    SELECT 
        c.chave_cliente,
        c.nome_cliente,
        c.segmento,
        COUNT(DISTINCT f.id_pedido) as total_pedidos,
        SUM(f.valor_venda) as total_gasto,
        ROUND(SUM(f.valor_venda) / COUNT(DISTINCT f.id_pedido), 2) as ticket_medio,
        ROUND(SUM(f.lucro) / SUM(f.valor_venda) * 100, 2) as margem_media
    FROM 
        fato.vendas f
    JOIN 
        dim.cliente c ON f.chave_cliente = c.chave_cliente
    GROUP BY 
        c.chave_cliente, c.nome_cliente, c.segmento
)
SELECT 
    nome_cliente,
    segmento,
    total_pedidos,
    total_gasto,
    ticket_medio,
    margem_media,
    CASE 
        WHEN total_pedidos > 10 AND total_gasto > 5000 THEN 'VIP'
        WHEN total_pedidos > 5 AND total_gasto > 2000 THEN 'Frequente'
        WHEN total_pedidos > 2 THEN 'Regular'
        ELSE 'Ocasional'
    END as categoria_cliente
FROM 
    metricas_cliente
ORDER BY 
    total_gasto DESC;
```

## Consultas para Gestão de Estoque (Simulado)

### 11. Produtos com Alta Demanda por Mês

```sql
SELECT 
    p.nome_produto,
    p.categoria,
    d.ano,
    d.mes,
    SUM(f.quantidade) as quantidade_vendida,
    ROUND(AVG(f.quantidade), 2) as quantidade_media_por_pedido
FROM 
    fato.vendas f
JOIN 
    dim.produto p ON f.chave_produto = p.chave_produto
JOIN 
    dim.data d ON f.chave_data = d.chave_data
GROUP BY 
    p.nome_produto, p.categoria, d.ano, d.mes
HAVING 
    SUM(f.quantidade) > 50
ORDER BY 
    d.ano, d.mes, quantidade_vendida DESC;
```

### 12. Análise de Sazonalidade de Produtos

```sql
SELECT 
    p.categoria,
    p.subcategoria,
    d.trimestre,
    SUM(f.valor_venda) as vendas_total,
    ROUND(SUM(f.valor_venda) / SUM(SUM(f.valor_venda)) OVER (PARTITION BY p.categoria, p.subcategoria) * 100, 2) as porcentagem_anual
FROM 
    fato.vendas f
JOIN 
    dim.produto p ON f.chave_produto = p.chave_produto
JOIN 
    dim.data d ON f.chave_data = d.chave_data
GROUP BY 
    p.categoria, p.subcategoria, d.trimestre
ORDER BY 
    p.categoria, p.subcategoria, d.trimestre;
```
