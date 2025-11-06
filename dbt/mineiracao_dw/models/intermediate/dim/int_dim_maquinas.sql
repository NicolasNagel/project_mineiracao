{{
    config(
        materialized = 'table',
        unique_key = 'sk_maquinas',
        tags = ['intermediate', 'dimension']
    )
}}

with maquinas as (
    select * from {{ ref('stg_maquinas') }}      
)

select {{ dbt_utils.generate_surrogate_key(['cod_maquina'])}} as fk_maquina
     , cod_maquina                     as id_maquina
     , nome                            as nm_maquina
     , fabricante                      as nm_fabricante
     , ano_fabricacao
     , date_trunc('day', dt_aquisicao) as dt_aquisicao
     , vlr_aquisicao
     , current_timestamp               as dbt_uploated_at
     , '{{ run_started_at }}'          as dbt_loaded_at

 from maquinas
