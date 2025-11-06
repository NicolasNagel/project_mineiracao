with source as (
    select * from {{ ref('dados_incidentes') }}
),

transformado as (
    select id as id_incidente
         , cod_maquina
         , cod_operador
         , data_ocorrencia as dt_ocorrencia
         , tipo as tp_incidente
         , gravidade
         , custo as vlr_custo
         , current_timestamp as etl_inserted_at

     from source
)

select * from transformado