// daily_visits_comments_charts
function dailyVC() {
	var daily_visits_comments_charts = echarts.init(document.getElementById('daily_visits_comments_charts'),'shine')
    // 指定图表的配置项和数据
    var option = {
        tooltip: {
            show:true,
        },
        legend: {
            data:[
                {
                    name:'Visits',
                },
                {
                    name:'Comments',
                },
            ],
        },
        xAxis: {
            data: ["2016/06/01","2016/06/02","2016/06/03","2016/06/04","2016/06/05","2016/06/06"]
        },
        yAxis: {},
        toolbox: {
            show: true,
            feature: {
                magicType: {type: ['line', 'bar']},
                restore: {},
                saveAsImage: {}
            }
        },
        series: [{
            name: 'Visits',
            type: 'bar',
            itemStyle: {
                    normal: {
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}'
                                }
                        }
            },
            data: [5, 20, 36, 10, 10, 20],
        },
                {
            name: 'Comments',
            type: 'bar',
            itemStyle: {
                    normal: {
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}'
                                }
                        }
            },
            data: [1, 11, 23, 4, 6, 15],
        },
        ],
        color:['#8ECF67','#1E91CF'],
    };
	// 使用刚指定的配置项和数据显示图表
    daily_visits_comments_charts.setOption(option);
}
// monthly_visits_comments_charts
function monthlyVC() {
	var monthly_visits_comments_charts = echarts.init(document.getElementById('monthly_visits_comments_charts'),'shine')
    // 指定图表的配置项和数据
    var option = {
        tooltip: {
            show:true,
        },
        legend: {
            data:[
                {
                    name:'Visits',
                },
                {
                    name:'Comments',
                },
            ],
        },
        xAxis: {
            data: ["2016/01","2016/02","2016/03","2016/04","2016/05","2016/06"]
        },
        yAxis: {},
        toolbox: {
            show: true,
            feature: {
                magicType: {type: ['line', 'bar']},
                restore: {},
                saveAsImage: {}
            }
        },
        series: [{
            name: 'Visits',
            type: 'bar',
            itemStyle: {
                    normal: {
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}'
                                }
                        }
            },
            data: [300, 150, 220, 250, 190, 200],
        },
                {
            name: 'Comments',
            type: 'bar',
            itemStyle: {
                    normal: {
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}'
                                }
                        }
            },
            data: [250, 125, 110, 200, 170, 150],
        },
        ],
        color:['#8ECF67','#1E91CF'],
    };
	// 使用刚指定的配置项和数据显示图表
    monthly_visits_comments_charts.setOption(option);
}
// visits_comments_likes_charts
function overview() {
	var visits_comments_likes_charts = echarts.init(document.getElementById('visits_comments_likes_charts'),'shine');
    var option = {
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['Visits','Comments','Likes']
        },
        series : [
            {
                name: 'amount',
                type: 'pie',
                radius : '55%',
                center: ['50%', '60%'],
                data:[
                    {value:335, name:'Visits'},
                    {value:310, name:'Comments'},
                    {value:234, name:'Likes'}
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ],
        color:['#8ECF67','#1E91CF','#FAC567'],
    };

    visits_comments_likes_charts.setOption(option);
}
// visits_china_map
function areaVisits() {
	var visits_china_map = echarts.init(document.getElementById('visits_china_map'),'shine');
    var option = {
        tooltip : {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data:['visits','comments']
        },
        visualMap: {
            min: 0,
            max: 2500,
            left: 'left',
            top: 'bottom',
            text:['高','低'],           // 文本，默认为数值文本
            calculable : true
        },
        toolbox: {
            show: true,
            orient : 'vertical',
            left: 'right',
            top: 'center',
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        series : [
            {
                name: 'visits',
                type: 'map',
                mapType: 'china',
                roam: false,
                label: {
                    normal: {
                        show: false
                    },
                    emphasis: {
                        show: true
                    }
                },
                data:[
                    {name: '北京',value: Math.round(Math.random()*1000)},
                    {name: '天津',value: Math.round(Math.random()*1000)},
                    {name: '上海',value: Math.round(Math.random()*1000)},
                    {name: '重庆',value: Math.round(Math.random()*1000)},
                    {name: '河北',value: Math.round(Math.random()*1000)},
                    {name: '河南',value: Math.round(Math.random()*1000)},
                    {name: '云南',value: Math.round(Math.random()*1000)},
                    {name: '辽宁',value: Math.round(Math.random()*1000)},
                    {name: '黑龙江',value: Math.round(Math.random()*1000)},
                    {name: '湖南',value: Math.round(Math.random()*1000)},
                    {name: '安徽',value: Math.round(Math.random()*1000)},
                    {name: '山东',value: Math.round(Math.random()*1000)},
                    {name: '新疆',value: Math.round(Math.random()*1000)},
                    {name: '江苏',value: Math.round(Math.random()*1000)},
                    {name: '浙江',value: Math.round(Math.random()*1000)},
                    {name: '江西',value: Math.round(Math.random()*1000)},
                    {name: '湖北',value: Math.round(Math.random()*1000)},
                    {name: '广西',value: Math.round(Math.random()*1000)},
                    {name: '甘肃',value: Math.round(Math.random()*1000)},
                    {name: '山西',value: Math.round(Math.random()*1000)},
                    {name: '内蒙古',value: Math.round(Math.random()*1000)},
                    {name: '陕西',value: Math.round(Math.random()*1000)},
                    {name: '吉林',value: Math.round(Math.random()*1000)},
                    {name: '福建',value: Math.round(Math.random()*1000)},
                    {name: '贵州',value: Math.round(Math.random()*1000)},
                    {name: '广东',value: Math.round(Math.random()*1000)},
                    {name: '青海',value: Math.round(Math.random()*1000)},
                    {name: '西藏',value: Math.round(Math.random()*1000)},
                    {name: '四川',value: Math.round(Math.random()*1000)},
                    {name: '宁夏',value: Math.round(Math.random()*1000)},
                    {name: '海南',value: Math.round(Math.random()*1000)},
                    {name: '台湾',value: Math.round(Math.random()*1000)},
                    {name: '香港',value: Math.round(Math.random()*1000)},
                    {name: '澳门',value: Math.round(Math.random()*1000)},
                ]
            },
            {
                name: 'comments',
                type: 'map',
                mapType: 'china',
                label: {
                    normal: {
                        show: false
                    },
                    emphasis: {
                        show: true
                    }
                },
                data:[
                    {name: '北京',value: Math.round(Math.random()*1000)},
                    {name: '天津',value: Math.round(Math.random()*1000)},
                    {name: '上海',value: Math.round(Math.random()*1000)},
                    {name: '重庆',value: Math.round(Math.random()*1000)},
                    {name: '河北',value: Math.round(Math.random()*1000)},
                    {name: '安徽',value: Math.round(Math.random()*1000)},
                    {name: '新疆',value: Math.round(Math.random()*1000)},
                    {name: '浙江',value: Math.round(Math.random()*1000)},
                    {name: '江西',value: Math.round(Math.random()*1000)},
                    {name: '山西',value: Math.round(Math.random()*1000)},
                    {name: '内蒙古',value: Math.round(Math.random()*1000)},
                    {name: '吉林',value: Math.round(Math.random()*1000)},
                    {name: '福建',value: Math.round(Math.random()*1000)},
                    {name: '广东',value: Math.round(Math.random()*1000)},
                    {name: '西藏',value: Math.round(Math.random()*1000)},
                    {name: '四川',value: Math.round(Math.random()*1000)},
                    {name: '宁夏',value: Math.round(Math.random()*1000)},
                    {name: '香港',value: Math.round(Math.random()*1000)},
                    {name: '澳门',value: Math.round(Math.random()*1000)}
                ]
            },

        ],
        color:['#8ECF67','#1E91CF'],
    };

    visits_china_map.setOption(option);
}

function visitsRank() {
	var visits_ranking = echarts.init(document.getElementById('visits_ranking'),'shine');
    // 指定图表的配置项和数据
    var option = {
        tooltip: {
            show:true,
        },
        legend: {
            data:[
                {
                    name:'Visits',
                },
            ],
        },
        xAxis: {
            data: ["北京","上海","广东","澳门","福建","珠海"]
        },
        yAxis: {},
        series: [{
            name: 'Visits',
            type: 'bar',
            itemStyle: {
                    normal: {
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}'
                                }
                        }
            },
            data: [10, 9, 8, 7, 6, 5],
        }
        ],
        color:['#1E91CF'],
    };

	// 使用刚指定的配置项和数据显示图表。
    visits_ranking.setOption(option);
}

$(function () {
	dailyVC();
	monthlyVC();
	overview();
	areaVisits();
	visitsRank();
});