create table СУДНО (
	ИДЕНТИФИКАТОР serial primary key,
	НАЗВАНИЕ varchar (50) not null,
	ПОРТ_ПРИПИСКИ varchar (50) not null,
	ЛЬГОТА smallint check(0 <= ЛЬГОТА and  ЛЬГОТА <= 100) 
);

create table МЕСТА_ПОГРУЗКИ (
	ИДЕНТИФИКАТОР serial primary key,
	ПРИЧАЛ varchar (50) not null,
	ПОРТ varchar (50) not null,
	ОТЧИСЛЕНИЯ_НА_ПОГРУЗКУ smallint check(0 <= ОТЧИСЛЕНИЯ_НА_ПОГРУЗКУ and  ОТЧИСЛЕНИЯ_НА_ПОГРУЗКУ <= 100)
);

create table ГРУЗ (
	ИДЕНТИФИКАТОР serial primary key,
	НАЗВАНИЕ varchar (50) not null,
	ПОРТ_СКЛАДИРОВАНИЯ varchar (50) not null,
	СТОИМОСТЬ integer check(0 <= СТОИМОСТЬ),
	МАКС_КОЛИЧЕСТВО smallint check(0 <= МАКС_КОЛИЧЕСТВО)
);

create type day_of_week as enum ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')

create table ПОГРУЗКА (
	НОМЕР_ВЕДОМОСТИ serial primary key,
	ДАТА day_of_week not null,
	СУДНО serial REFERENCES СУДНО (ИДЕНТИФИКАТОР),
	МЕСТА_ПОГРУЗКИ serial REFERENCES МЕСТА_ПОГРУЗКИ (ИДЕНТИФИКАТОР),
	ГРУЗ serial REFERENCES ГРУЗ (ИДЕНТИФИКАТОР),
	КОЛИЧЕСТВО smallint check(0 <= КОЛИЧЕСТВО),
	СТОИМОСТЬ integer check(0 <= СТОИМОСТЬ)
);