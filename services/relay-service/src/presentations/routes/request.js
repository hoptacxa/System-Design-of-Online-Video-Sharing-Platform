const requestController = require('../controllers/requestController.js');

function requestRoute(ws, data) {
    requestController(ws, data);
}

module.exports = requestRoute;