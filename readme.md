# abracadabra

# Run

### Console Command:

To process all files in the ./data/ directory:
```shell
python main.py ./data/*
```

```

Total requests: 456314

HANDLER              DEBUG    INFO     WARNING  ERROR    CRITICAL  
-------------------------------------------------------------------
/api/v1/reviews/     0        48397    0        20737    0         
/admin/dashboard/    0        20746    0        6915     0         
/api/v1/users/       0        13831    0        6914     0         
/api/v1/cart/        0        34564    0        6912     0         
/api/v1/products/    0        27656    0        13827    0         
/api/v1/support/     0        48393    0        6915     0         
/api/v1/auth/login/  0        34567    0        6913     0         
/admin/login/        0        27656    0        13826    0         
/api/v1/checkout/    0        27659    0        13826    0         
/api/v1/payments/    0        13834    0        2        0         
/api/v1/orders/      0        27654    0        6915     0         
/api/v1/shipping/    0        20741    0        6914     0 
```
### Saving Output to a File:

Use the --report handlers flag to save the output to a file:
```shell
python main.py ./data/* --report handlers
```

```
$ ls -lah | grep han
-rw-r--r-- 1 g g  977 13 19:04 handlers
```

### Default Behavior:

If the `--report` flag is **not** set to `handlers`, the output will be displayed in the console.