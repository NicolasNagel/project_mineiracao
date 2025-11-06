with source as (
    select * from {{ ref('dados_manutencoes') }}
),

transformado as (
    select id as id_manutencao
         , cod_maquina
         , tipo as tp_manutencao
         , data_inicio as dt_inicio
         , data_fim as dt_fim
         , tempo_parada_horas
         , gravidade
         , custo as vlr_custo
         , current_timestamp as etl_inserted_at

     from source
)

select * from transformado