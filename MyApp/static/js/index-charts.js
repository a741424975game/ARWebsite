function monthlyVisits() {
	var monthly_visits = echarts.init(document.getElementById('monthly-visits'),'shine')
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
        ],
        color:['#8ECF67'],
    };
	// 使用刚指定的配置项和数据显示图表
    monthly_visits.setOption(option);
}

function regionRank() {
	var region_rank = echarts.init(document.getElementById('region-rank'),'shine');
    // 指定图表的配置项和数据
    var option = {
        tooltip: {
            show:true,
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
    region_rank.setOption(option);
}

$(function () {
	monthlyVisits();
	regionRank();
});