# opulence-web

## Project setup
##### Installs back-end flask server dependencies

```zsh
pip install -r requirements.txt
```

##### Installs front-end dependencies
```zsh
npm install
```


## Running Locally
```zsh
# Runs flask back-end server
python main.py

# Start redis for turn timers to work
docker run -d -p 6379:6379 redis

# Compiles and hot-reloads for development and runs front-end web server
npm run serve
```

## Building for Production
```zsh
# Compiles and minifies for production
npm run build
```


```zsh
# Lints and fixes files
npm run lint
```

##### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
