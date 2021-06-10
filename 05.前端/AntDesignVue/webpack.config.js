var path = require('path'); //引文文件路径
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: ['./src/index.js'], //入口文件
    output: {
        path: path.join(__dirname, 'dist'), //打包出口文件路径
        filename: 'index.js' //打包文件名
    },
    module: {
        rules: [{
            test: /\.less$/,
            use: ExtractTextPlugin.extract({
                use: [{
                    loader: 'css-loader?importLoaders=true',
                }, {
                    loader: "less-loader",
                    options: {
                        modifyVars: {
                            'primary-color': '#2649e8',
                        },
                        javascriptEnabled: true,
                    }
                }]
            })
        }]
    },
    plugins: [
        new ExtractTextPlugin("styles.css"),
        new HtmlWebpackPlugin({
            template: './src/index.html', //模板路径
            filename: "index.html",
            inject: false,
        }),
    ],
}