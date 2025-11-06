{{
    config(
        materialized = 'table',
        unique_key = 'sk_operador',
        tags = ['intermediate', 'dimension']
    )
}}

with operadores as (
    select * from {{ ref('stg_operadores') }}
)

select {{ dbt_utils.generate_surrogate_key(['cod_operador']) }} as sk_operador
     , id_operador
     , nome                                                     as nm_operador
     , setor
     , nivel_experiencia
     , current_timestamp                                        as etl_uploaded_at
     , '{{ run_started_at }}'                                   as etl_inserted_at

 from operadores