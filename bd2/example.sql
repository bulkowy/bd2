
INSERT INTO "app_permission" ("name") VALUES ('test') RETURNING "app_permission"."id";

INSERT INTO "app_substitutionreason" ("desc") VALUES ('test') RETURNING "app_substitutionreason"."id";

-- permissionchangereason insert
INSERT INTO "app_permissionchangereason" ("desc") VALUES ('test') RETURNING "app_permissionchangereason"."id";

-- position insert
INSERT INTO "app_position" ("name") VALUES ('test2') RETURNING "app_position"."id";
SELECT "app_permission"."id" FROM "app_permission" 
    INNER JOIN "app_position_permissions" ON ("app_permission"."id" = "app_position_permissions"."permission_id") 
        WHERE "app_position_permissions"."position_id" = 12;
SELECT "app_position_permissions"."permission_id" FROM "app_position_permissions" 
    WHERE ("app_position_permissions"."permission_id" IN (1, 2, 3, 4) AND "app_position_permissions"."position_id" = 12);
INSERT INTO "app_position_permissions" ("position_id", "permission_id") VALUES (12, 1), (12, 2), (12, 3), (12, 4) RETURNING "app_position_permissions"."id";

-- sub insert
INSERT INTO "app_substitution" ("substitute_begin", "substitute_end", "substituted_worker_id", "substituting_worker_id", "reason_id") 
    VALUES ('2019-05-21'::date, '2019-05-21'::date, 100, 200, 2) RETURNING "app_substitution"."id";

-- worker insert
INSERT INTO "app_worker" ("supervisor_id", "name", "surname", "pesel", "salary", "position_id", "employment_date", "promotion_date") 
    VALUES (1, 'test', 'test', '98765432101', 123321, 1, '2019-05-21'::date, '2019-05-21'::date) RETURNING "app_worker"."id";