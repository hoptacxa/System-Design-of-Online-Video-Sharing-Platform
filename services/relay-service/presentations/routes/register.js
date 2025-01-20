const registerController = require('../controllers/registerController.js');

function registerRoute(ws, data) {
    registerController(ws, data);
}

module.exports = registerRoute;