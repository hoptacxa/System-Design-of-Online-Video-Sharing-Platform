const responseController = require('../controllers/responseController.js');

function responseRoute(ws, data) {
    responseController(ws, data);
}

module.exports = responseRoute;