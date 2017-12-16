CREATE TABLE "Question" (
	"id" serial NOT NULL,
	"name" serial NOT NULL,
	"content" serial NOT NULL,
	CONSTRAINT Question_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Category" (
	"name" serial NOT NULL,
	CONSTRAINT Category_pk PRIMARY KEY ("name")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Questions_Categories" (
	"category.name" TEXT NOT NULL,
	"question.id" int NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Answer" (
	"id" serial NOT NULL,
	"content" TEXT NOT NULL,
	"question.id" int NOT NULL,
	CONSTRAINT Answer_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Language" (
	"id" serial NOT NULL,
	"name" TEXT NOT NULL,
	"version" TEXT NOT NULL,
	CONSTRAINT Language_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Answers_Languages" (
	"answer.id" int NOT NULL,
	"language.id" int NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Hint" (
	"id" int NOT NULL,
	"order" int NOT NULL,
	"content" TEXT NOT NULL,
	"question.id" int NOT NULL,
	CONSTRAINT Hint_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);





ALTER TABLE "Questions_Categories" ADD CONSTRAINT "Questions_Categories_fk0" FOREIGN KEY ("category.name") REFERENCES "Category"("name");
ALTER TABLE "Questions_Categories" ADD CONSTRAINT "Questions_Categories_fk1" FOREIGN KEY ("question.id") REFERENCES "Question"("id");

ALTER TABLE "Answer" ADD CONSTRAINT "Answer_fk0" FOREIGN KEY ("question.id") REFERENCES "Question"("id");


ALTER TABLE "Answers_Languages" ADD CONSTRAINT "Answers_Languages_fk0" FOREIGN KEY ("answer.id") REFERENCES "Answer"("id");
ALTER TABLE "Answers_Languages" ADD CONSTRAINT "Answers_Languages_fk1" FOREIGN KEY ("language.id") REFERENCES "Language"("id");

ALTER TABLE "Hint" ADD CONSTRAINT "Hint_fk0" FOREIGN KEY ("question.id") REFERENCES "Question"("id");

