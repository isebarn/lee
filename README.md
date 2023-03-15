3 Endpoints

# View clicks table
```
GET https://lee-stage.us.aldryn.io
```

Returns an html table with everything from the `Clicks` database table

# Add site
```
POST https://lee-stage.us.aldryn.io/add_site
{
    name: youtube
    url: "https://www.youtube.com/"
}
```

# Add to Clicks table
```
GET https://lee-stage.us.aldryn.io/click?n=Frank&s=youtube
```

Redirects to whatever site matches the `s` parameter to the `Sites.name` property


