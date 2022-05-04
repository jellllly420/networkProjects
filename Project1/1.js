const express = require('express')
const path = require('path')

const content = express()
content.use(express.static(path.join(__dirname, 'save')))

content.listen(8080, () => {
    console.log('Listening at port 8080...')
})