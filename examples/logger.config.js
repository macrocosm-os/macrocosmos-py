module.exports = {
    apps: [{
        name: 'macrocosmos-logger',
        script: 'uv',
        args: 'run logger_example.py',
        autorestart: false,
        max_restarts: 0,
        env: {
            MACROCOSMOS_BASE_URL: 'localhost:4000',
            MACROCOSMOS_CAPTURE_LOGS: 'true',
            MACROCOSMOS_USE_HTTPS: 'false'
        }
    }]
}
