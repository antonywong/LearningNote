var fs = require('fs');
var sqlite3 = require('sqlite3').verbose();

module.exports = function () {
    var dbFile = process.argv[2];
    var DB = {};

    DB.db = new sqlite3.Database(dbFile);

    DB.exist = fs.existsSync(dbFile);
    if (!DB.exist) {
        console.log("No db file:" + dbFile);
    };

    this.query = (sql) => {
        return new Promise((resolve, reject) => {
            DB.db.all(sql, (err, rows) => {
                if (null != err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        })
    };

    this.run = (sql, paras) => {
        return new Promise((resolve, reject) => {
            if (paras) {
                DB.db.serialize(() => {
                    var stmt = DB.db.prepare(sql);
                    for (var para of paras) {
                        stmt.run(para);
                    }
                    stmt.finalize();
                    resolve();
                });
            } else {
                DB.db.run(sql, function (err) {
                    if (null != err) {
                        reject(err);
                    } else {
                        resolve();
                    }
                });
            }
        })
    };

    this.close = () => {
        DB.db.close();
    }
};