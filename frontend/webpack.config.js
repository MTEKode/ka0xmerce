const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const path = require('path');

const resolve = path.resolve.bind(path, __dirname);
const debug = process.env.NODE_ENV === 'production' ? 'production' : 'development';

const entryItems = {
    'starboy.lvh.me': './starboy.lvh.me/js/storefront.js',
    'emeraldlion.lvh.me': './emeraldlion.lvh.me/js/storefront.js'
};

const extractCssPlugin = new MiniCssExtractPlugin({
    filename: '[name]/storefront.css',
    chunkFilename: '[name]/storefront.css',
});

const config = {
    mode: debug,
    entry: entryItems,
    output: {
        path: resolve('../flaskshop/static/build/'),
        filename: '[name]/storefront.js',
        chunkFilename: '[name]/storefront.js'
    },
    devServer: {
        headers: {'Access-Control-Allow-Origin': '*'},
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true,
                        },
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true,
                        },
                    },
                ],
            },
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader']
            },
            {
                test: /\.(eot|otf|png|svg|jpg|ttf|woff|woff2)(\?v=[0-9.]+)?$/,
                type: "javascript/auto",
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            esModule: false,
                            name: '[name].[ext]',
                            outputPath: (url, resourcePath, context) => {
                                const [frontendDir, projectDir] = ['frontend', 'flaskshop/static'];
                                const relativePath = path.relative(frontendDir, resourcePath);
                                const [directory] = relativePath.split(path.sep);
                                return path.join(projectDir, 'build', directory, url);
                            },
                        },
                    },
                ],
                include: [
                    resolve('node_modules'),
                    resolve('fonts'),
                    resolve('images'),
                ],
            },
        ],
    },
    plugins: [
        extractCssPlugin,
    ],
    optimization: {
        minimizer: [new TerserPlugin({
            extractComments: false,
            terserOptions: {
                format: {
                    comments: false,
                },
            },
        })],
    },
    performance: {
        hints: false,
        maxEntrypointSize: 512000,
        maxAssetSize: 512000
    },
};

module.exports = config;
