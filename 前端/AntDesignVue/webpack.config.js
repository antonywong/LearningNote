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
        rules: [
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: "css-loader"
                })

            }, {//正则匹配后缀.less文件;
                test: /\.less$/,
                //使用html-webpack-plugin插件独立css到一个文件;
                use: ExtractTextPlugin.extract({
                    use: [{
                        loader: 'css-loader?importLoaders=true',
                    },
                        //加载less-loader同时也得安装less;
                        "less-loader"
                    ]
                })
            },
        ]
    },
    plugins: [
        new ExtractTextPlugin("styles.css"),
        new HtmlWebpackPlugin({
            template: './src/index.html', //模板路径
            filename: "index.html",
            inject: false,
        }),
    ],
    devServer: {
        //配置nodejs本地服务器，
        contentBase: './dist',
        hot: true //本地服务器热更新
    },
    resolve: {
        //设置可省略文件后缀名(注:如果有文件没有后缀设置‘’会在编译时会报错,必须改成' '中间加个空格。ps:虽然看起来很强大但有时候省略后缀真不知道加载是啥啊~);
        extensions: [' ', '.css', '.scss', '.sass', '.less', '.js', '.json'],
        //查找module的话从这里开始查找;
        modules: [path.resolve(__dirname, "src"), "node_modules"], //绝对路径;
        //别名设置,主要是为了配和webpack.ProvidePlugin设置全局插件;
        alias: {
            //设置全局jquery插件;
        }
    }
}