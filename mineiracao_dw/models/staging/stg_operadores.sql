with source as (
    select * from {{ ref('dados_operadores') }}
),

transformado as (
    select id as id_operador
         , matricula as cod_operador
         , nome
         , setor
         , nivel_experiencia
         , current_timestamp as etl_inserted_at

     from source
)

select * from transformado