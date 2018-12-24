word_cloud_head = '''
<html>
    <head>
        <meta charset="utf-8">
        <script src='https://cdn.bootcss.com/echarts/3.7.0/echarts.simple.js'></script>
        <script src='../dist/echarts-wordcloud.js'></script>
    </head>
    <body>
        <style>
            html, body, #main {
                width: 100%;
                height: 100%;
                margin: 0;
            }
        </style>
        <div id='main'></div>
        <script>
            var chart = echarts.init(document.getElementById('main'));

            var option = {
                tooltip: {},
                series: [ {
                    type: 'wordCloud',
                    gridSize: 2,
                    sizeRange: [12, 50],
                    rotationRange: [-90, 90],
                    shape: 'pentagon',
                    width: 600,
                    height: 400,
                    drawOutOfBound: true,
                    textStyle: {
                        normal: {
                            color: function () {
                                return 'rgb(' + [
                                    Math.round(Math.random() * 160),
                                    Math.round(Math.random() * 160),
                                    Math.round(Math.random() * 160)
                                ].join(',') + ')';
                            }
                        },
                        emphasis: {
                            shadowBlur: 10,
                            shadowColor: '#333'
                        }
                    },
                    data: [
                        '''

word_cloud_tail =  '''
                    ]
                } ]
            };

            chart.setOption(option);

            window.onresize = chart.resize;
        </script>
    </body>
</html>'''
