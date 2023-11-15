import sandbox as s



if s.env == 'sandbox':
   import test_1 as t
elif s.env == 'dev':
   import test_2 as t
elif s.env == 'prod':
   import test_3 as t


print(t.string)

