var dal = require('../../dal/main');

module.exports = {
    singin: (req, res) => {
        var db = new dal();

        var sql = "select * from User where account='" + req.body.account + "' and password='" + req.body.password + "'";
        db.query(sql)
            .then((rows) => {
                if (rows.length == 1) {
                    var result = { token: rows[0].id, amount: rows[0].amount }
                    res.send(result);
                }
                res.end();
            })
            .catch((err) => { res.send(err); res.end(); })
            .finally(() => { db.close(); });
    },
    postAmount: (req, res) => {
        var db = new dal();

        var sql = "update User set amount=" + req.body.amount + " where id=" + req.body.token;
        db.run(sql)
            .then(() => { res.end(); })
            .catch((err) => { res.send(err); res.end(); })
            .finally(() => { db.close(); });
    }
};