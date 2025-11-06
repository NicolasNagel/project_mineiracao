with source as (
    select * from {{ ref('dados_maquinas') }}
),

transformado as (
    select id as id_maquina
         , codigo as cod_maquina
         , nome
         , fabricante
         , ano_fabricacao
         , data_aquisicao as dt_aquisicao
         , valor_aquisicao as vlr_aquisicao
         , current_timestamp as elt_inserted_at
     from source
)

select * from transformado