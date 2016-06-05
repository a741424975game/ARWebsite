function monthlyVisits() {
	var monthly_visits = echarts.init(document.getElementById('monthly-visits'),'shine')
    // 指定图表的配置项和数据
    var option = {
        tooltip: {
            show:true,
        },
        xAxis: {
            data: recently_months,
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
            data: recently_months_visits_amount,
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
            data: area_visits_ranking,
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
            data: area_visits_ranking_data,
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