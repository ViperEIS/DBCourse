--a
select НАЗВАНИЕ, СТОИМОСТЬ from ГРУЗ where МАКС_КОЛИЧЕСТВО < 500;

--b
select distinct ПОРТ from МЕСТА_ПОГРУЗКИ where ПРИЧАЛ like '%N%' or ОТЧИСЛЕНИЯ_НА_ПОГРУЗКУ > 5;

--c
select НАЗВАНИЕ from СУДНО where ПОРТ_ПРИПИСКИ = 'Одесса';