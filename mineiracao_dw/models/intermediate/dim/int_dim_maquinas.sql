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