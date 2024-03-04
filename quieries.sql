SELECT
  "shopapp_product"."id",
  "shopapp_product"."name",
  "shopapp_product"."description",
  "shopapp_product"."price",
  "shopapp_product"."created_by_id",
  "shopapp_product"."discount",
  "shopapp_product"."create_at",
  "shopapp_product"."archive",
  "shopapp_product"."preview"
FROM
  "shopapp_product"
WHERE
  NOT "shopapp_product"."archive"
ORDER BY
  "shopapp_product"."name" ASC,
  "shopapp_product"."price" ASC;

--
SELECT
  "shopapp_product"."id",
  "shopapp_product"."name",
  "shopapp_product"."description",
  "shopapp_product"."price",
  "shopapp_product"."created_by_id",
  "shopapp_product"."discount",
  "shopapp_product"."create_at",
  "shopapp_product"."archive",
  "shopapp_product"."preview"
FROM
  "shopapp_product"
WHERE
  "shopapp_product"."id" = 14
LIMIT 21;
args =(14,);
alias=default
--
SELECT
  "shopapp_productimage"."id",
  "shopapp_productimage"."product_id",
  "shopapp_productimage"."image",
  "shopapp_productimage"."description"
FROM
  "shopapp_productimage"
WHERE
  "shopapp_productimage"."product_id" IN (14);
args =(14,);
alias = default
--
SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT 21;
args =(1,);
alias=default
--
SELECT
  "shopapp_order"."id",
  "shopapp_order"."delivery_adress",
  "shopapp_order"."promocode",
  "shopapp_order"."created_at",
  "shopapp_order"."user_id",
  "shopapp_order"."archive",
  "shopapp_order"."receipt",
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "shopapp_order"
  INNER JOIN "auth_user" ON (
      "shopapp_order"."user_id" = "auth_user"."id"
    )
WHERE
  "shopapp_order"."id" = 31
LIMIT 21;
args =(31,);
alias=default
--
SELECT
  ("shopapp_order_products"."order_id") AS "_prefetch_related_val_order_id",
  "shopapp_product"."id",
  "shopapp_product"."name",
  "shopapp_product"."description",
  "shopapp_product"."price",
  "shopapp_product"."created_by_id",
  "shopapp_product"."discount",
  "shopapp_product"."create_at",
  "shopapp_product"."archive",
  "shopapp_product"."preview"
FROM
  "shopapp_product"
  INNER JOIN "shopapp_order_products" ON (
      "shopapp_product"."id" = "shopapp_order_products"."product_id"
    )
WHERE
  "shopapp_order_products"."order_id" IN (31)
ORDER BY
  "shopapp_product"."name" ASC,
  "shopapp_product"."price" ASC;
args =(31,);
alias = default
--
SELECT
  "django_session"."session_key",
  "django_session"."session_data",
  "django_session"."expire_date"
FROM
  "django_session"
WHERE
  (
    "django_session"."expire_date" > '2024-02-22 14:16:33.773076'
    AND "django_session"."session_key" = 'j1yl4u5ty74tto4eee94xllkbw439abz'
  )
LIMIT 21;
args =('2024-02-22 14:16:33.773076', 'j1yl4u5ty74tto4eee94xllkbw439abz');
alias=default
SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT 21;
args =(1,);
alias=default
SELECT
  "shopapp_order"."id",
  "shopapp_order"."delivery_adress",
  "shopapp_order"."promocode",
  "shopapp_order"."created_at",
  "shopapp_order"."user_id",
  "shopapp_order"."archive",
  "shopapp_order"."receipt",
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "shopapp_order"
  INNER JOIN "auth_user" ON (
      "shopapp_order"."user_id" = "auth_user"."id"
    )
WHERE
  "shopapp_order"."id" = 31
LIMIT 21;

SELECT
  ("shopapp_order_products"."order_id") AS "_prefetch_related_val_order_id",
  "shopapp_product"."id",
  "shopapp_product"."name",
  "shopapp_product"."description",
  "shopapp_product"."price",
  "shopapp_product"."created_by_id",
  "shopapp_product"."discount",
  "shopapp_product"."create_at",
  "shopapp_product"."archive",
  "shopapp_product"."preview"
FROM
  "shopapp_product"
  INNER JOIN "shopapp_order_products" ON (
      "shopapp_product"."id" = "shopapp_order_products"."product_id"
    )
WHERE
  "shopapp_order_products"."order_id" IN (31)
ORDER BY
  "shopapp_product"."name" ASC,
  "shopapp_product"."price" ASC;

SELECT
  "django_session"."session_key",
  "django_session"."session_data",
  "django_session"."expire_date"
FROM
  "django_session"
WHERE
  (
    "django_session"."expire_date" > '2024-02-22 14:28:21.043313'
    AND "django_session"."session_key" = 'j1yl4u5ty74tto4eee94xllkbw439abz'
  )
LIMIT 21;

SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT 21;

SELECT
  "shopapp_order"."id",
  "shopapp_order"."delivery_adress",
  "shopapp_order"."promocode",
  "shopapp_order"."created_at",
  "shopapp_order"."user_id",
  "shopapp_order"."archive",
  "shopapp_order"."receipt",
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "shopapp_order"
  INNER JOIN "auth_user" ON (
      "shopapp_order"."user_id" = "auth_user"."id"
    )
WHERE
  NOT "shopapp_order"."archive"
ORDER BY
  "shopapp_order"."user_id" ASC;

SELECT
  ("shopapp_order_products"."order_id") AS "_prefetch_related_val_order_id",
  "shopapp_product"."id",
  "shopapp_product"."name",
  "shopapp_product"."description",
  "shopapp_product"."price",
  "shopapp_product"."created_by_id",
  "shopapp_product"."discount",
  "shopapp_product"."create_at",
  "shopapp_product"."archive",
  "shopapp_product"."preview"
FROM
  "shopapp_product"
  INNER JOIN "shopapp_order_products" ON (
      "shopapp_product"."id" = "shopapp_order_products"."product_id"
    )
WHERE
  "shopapp_order_products"."order_id" IN (2,30,31)
ORDER BY
  "shopapp_product"."name" ASC,
  "shopapp_product"."price" ASC;

SELECT
  "shopapp_order"."id",
  "shopapp_order"."delivery_adress",
  "shopapp_order"."promocode",
  "shopapp_order"."created_at",
  "shopapp_order"."user_id",
  "shopapp_order"."archive",
  "shopapp_order"."receipt",
  (CAST(SUM("shopapp_product"."price") AS NUMERIC)) AS "total",
  COUNT("shopapp_order_products"."product_id") AS "products_count"
FROM
  "shopapp_order"
  LEFT OUTER JOIN "shopapp_order_products" ON (
      "shopapp_order"."id" = "shopapp_order_products"."order_id"
    )
  LEFT OUTER JOIN "shopapp_product" ON (
      "shopapp_order_products"."product_id" = "shopapp_product"."id"
    )
GROUP BY
  "shopapp_order"."id",
  "shopapp_order"."delivery_adress",
  "shopapp_order"."promocode",
  "shopapp_order"."created_at",
  "shopapp_order"."user_id",
  "shopapp_order"."archive",
  "shopapp_order"."receipt";

