--a
select distinct
	ПОРТ_ПРИПИСКИ
from
	ПОГРУЗКА 
	inner join (select ИДЕНТИФИКАТОР, ПОРТ_ПРИПИСКИ from СУДНО) as с
		on СУДНО = ИДЕНТИФИКАТОР
where 
	ДАТА = 'Среда' and 
	СТОИМОСТЬ >= all (select СТОИМОСТЬ from ПОГРУЗКА where ДАТА = 'Среда');
	
--b
select distinct
	г.НАЗВАНИЕ
from
	ПОГРУЗКА 
	inner join (select ИДЕНТИФИКАТОР, ПОРТ_ПРИПИСКИ from СУДНО) as с
		on СУДНО = ИДЕНТИФИКАТОР
	inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ from ГРУЗ) as г
		on ГРУЗ = г.ИДЕНТИФИКАТОР
where 
	ПОРТ_ПРИПИСКИ = 'Владивосток' and
	ПОГРУЗКА.КОЛИЧЕСТВО = any (select КОЛИЧЕСТВО from ПОГРУЗКА where КОЛИЧЕСТВО > 20);

--с
select 
	ПРИЧАЛ
from
	МЕСТА_ПОГРУЗКИ
where
	ПРИЧАЛ = any (
	select 
		ПРИЧАЛ
	from
		(select
			ПРИЧАЛ, count(*) as КОЛИЧЕСТВО_ПОГРУЗОК
		from
			(select
				*
			from
				ПОГРУЗКА 
				inner join (select ИДЕНТИФИКАТОР, ПРИЧАЛ, ОТЧИСЛЕНИЯ_НА_ПОГРУЗКУ from МЕСТА_ПОГРУЗКИ) as м
					on МЕСТА_ПОГРУЗКИ = ИДЕНТИФИКАТОР
			where 
				СТОИМОСТЬ = any (select СТОИМОСТЬ from ПОГРУЗКА where СТОИМОСТЬ > 500000)) as foo
		group by ПРИЧАЛ) as foo
	where КОЛИЧЕСТВО_ПОГРУЗОК = any (select КОЛИЧЕСТВО from ПОГРУЗКА where КОЛИЧЕСТВО >= 2)
	)
order by ОТЧИСЛЕНИЯ_НА_ПОГРУЗКУ limit 1;

--d
select 
	НАЗВАНИЕ,
	ПОРТ_ПРИПИСКИ,
	ПОРТ
from
	ПОГРУЗКА 
	inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ, ПОРТ_ПРИПИСКИ from СУДНО) as с
		on СУДНО = ИДЕНТИФИКАТОР
	inner join (select ИДЕНТИФИКАТОР, ПОРТ from МЕСТА_ПОГРУЗКИ) as м
		on МЕСТА_ПОГРУЗКИ = м.ИДЕНТИФИКАТОР
where СТОИМОСТЬ = any (select СТОИМОСТЬ from ПОГРУЗКА where СТОИМОСТЬ > 50000);



