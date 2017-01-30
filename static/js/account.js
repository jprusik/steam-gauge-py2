function tableTotals(data_set){
        var totals = {
            'app_count':0,
            'minutes_total':0,
            'minutes_average':0,
            'hours_total':0,
            'hours_average':0,
            'price_total':0,
            'price_average':0,
            'price_hours_total':0,
            'average_metascore':0,
            'metascore_count':0,
            'windows_total':0,
            'mac_total':0,
            'linux_total':0,
            'mb_install_total':0,
            'mb_install_average':0,
            'gb_install_total':0,
            'gb_install_average':0,
            'controller_total':0,
            'multiplayer_total':0
        };

        $.each(data_set, function(i,v){
            if ($.isNumeric(v[4])){
                totals.minutes_total += parseInt(v[4]);
            }
            if ($.isNumeric(v[5])){
                totals.hours_total += parseFloat(v[5]);
            }
            if ($.isNumeric(v[6])){
                totals.price_total += parseFloat(v[6]);
            }
            if ($.isNumeric(v[11].split(/<\/|\">/)[1])){
                totals.metascore_count += 1;
                totals.average_metascore += parseInt(v[11].split(/<\/|\">/)[1]);
            }
            if (v[12].split(/<\/span|none;\">/)[1] === '1'){
                totals.windows_total += 1;
            }
            if (v[13].split(/<\/span|none;\">/)[1] === '1'){
                totals.mac_total += 1;
            }
            if (v[14].split(/<\/span|none;\">/)[1] === '1'){
                totals.linux_total += 1;
            }
            if ($.isNumeric(v[15])){
                totals.mb_install_total += parseInt(v[15]);
            }
            if ($.isNumeric(v[16])){
                totals.gb_install_total += parseFloat(v[16]);
            }
            if ((v[17] === 'full') || (v[17] === 'partial')){
                totals.controller_total += 1;
            }
            if (v[18].split(/<\/span|none;\">/)[1] === '1'){
                totals.multiplayer_total += 1;
            }
        });
        totals.app_count = data_set.length;
        totals.average_metascore /= totals.metascore_count;
        totals.average_metascore = parseInt(totals.average_metascore);
        if (!$.isNumeric(totals.average_metascore)){
            totals.average_metascore = 0;
        }
        totals.price_average = Math.round((totals.price_total/totals.app_count)*100)/100;
        if (!$.isNumeric(totals.price_average)){
            totals.price_average = 0;
        }
        totals.price_total = Math.round(totals.price_total*100)/100;
        totals.minutes_average = Math.round((totals.minutes_total/totals.app_count)*10)/10;
        if (!$.isNumeric(totals.minutes_average)){
            totals.minutes_average = 0;
        }
        totals.hours_total = Math.round(totals.hours_total*10)/10;
        totals.hours_average = Math.round((totals.hours_total/totals.app_count)*10)/10;
        if (!$.isNumeric(totals.hours_average)){
            totals.hours_average = 0;
        }
        totals.gb_install_total = Math.round(totals.gb_install_total*10)/10;
        totals.gb_install_average = Math.round((totals.gb_install_total/totals.app_count)*10)/10;
        if (!$.isNumeric(totals.gb_install_average)){
            totals.gb_install_average = 0;
        }
        totals.mb_install_average = Math.round((totals.mb_install_total/totals.app_count)*10)/10;
        if (!$.isNumeric(totals.mb_install_average)){
            totals.mb_install_average = 0;
        }
        totals.price_hours_total = Math.round((totals.price_total/totals.hours_total)*10)/10;
        return totals;
    }

    function updateFields(totals_json){
        $('#type_footer').html('Totals:');
        // $('#id_footer').html(totals_json.);
        // $('#icon_footer').html(totals_json.);
        $('.title_sum').html(totals_json.app_count +' selected');
        $('.minutes_played_sum').html('<div style="white-space:nowrap;">'+totals_json.minutes_total+' min (total)</div><div style="margin-top:0.75em;white-space:nowrap;">'+totals_json.minutes_average+' min (avg)</div>');
        $('.hours_played_sum').html('<div style="white-space:nowrap;">'+totals_json.hours_total+' hrs (total)</div><div style="margin-top:0.75em;white-space:nowrap;">'+totals_json.hours_average+' hrs (avg)</div>');
        $('.store_price_default_usd_sum').html('<div style="white-space:nowrap;">$'+totals_json.price_total+' (total)</div><div style="margin-top:0.75em;white-space:nowrap;">$'+totals_json.price_average+' (avg)</div>');
        $('.price_hours_sum').html(totals_json.price_hours_total+' $/hrs');
        // $('#release_date_footer').html(totals_json.);
        // $('#developer_footer').html(totals_json.);
        // $('#publisher_footer').html(totals_json.);
        $('.metascore_sum').html(totals_json.average_metascore+' (avg)');
        $('.os_windows_sum').html(totals_json.windows_total);
        $('.os_mac_sum').html(totals_json.mac_total);
        $('.os_linux_sum').html(totals_json.linux_total);
        $('.size_mb_sum').html('<div style="white-space:nowrap;">'+totals_json.mb_install_total+' MB (total)</div><div style="margin-top:0.75em;white-space:nowrap;">'+totals_json.mb_install_average+' MB (avg)</div>');
        $('.size_gb_sum').html('<div style="white-space:nowrap;">'+totals_json.gb_install_total+' GB (total)</div><div style="margin-top:0.75em;white-space:nowrap;">'+totals_json.gb_install_average+' GB (avg)</div>');
        $('.controller_support_sum').html(totals_json.controller_total);
        $('.multiplayer_sum').html(totals_json.multiplayer_total);
        // $('#genres_footer').html(totals_json.);

        // Update Summary Message
        $('.hours_played_container').html(totals_json.hours_total);
        $('.selection_count_container').html(totals_json.app_count);
        $('.usd_sum_container').html(totals_json.price_total);
        $('.gb_sum_container').html(totals_json.gb_install_total);
    }

    function timeSince(date) {
        var seconds = Math.floor((new Date() - date) / 1000);
        var interval = Math.floor(seconds / 31536000);
        if (interval > 1) {
            return interval + " years";
        }
        interval = Math.floor(seconds / 2592000);
        if (interval > 1) {
            return interval + " months";
        }
        interval = Math.floor(seconds / 86400);
        if (interval > 1) {
            return interval + " days";
        }
        interval = Math.floor(seconds / 3600);
        if (interval > 1) {
            return interval + " hours";
        }
        interval = Math.floor(seconds / 60);
        if (interval > 1) {
            return interval + " minutes";
        }
        return Math.floor(seconds) + " seconds";
    }

    function selectionPreset(preset){
        var all_rows = oTable.fnGetNodes();
        var table_instance = TableTools.fnGetInstance('app_list');
        if (preset === 'invert'){
            $.each(all_rows, function(i,v){
                if (table_instance.fnIsSelected(v)){
                    table_instance.fnDeselect(v);
                }
                else{
                    table_instance.fnSelect(v);
                }
            });
        }
        if (preset === 'played'){
            $.each(all_rows, function(i,v){
                if (parseFloat($(v).children('.hours_played_col').text())>0){
                    table_instance.fnSelect(v);
                }
            });
        }
        if (preset === 'games'){
            $.each(all_rows, function(i,v){
                if ($(v).children('.type_col').text() === 'Game'){
                    table_instance.fnSelect(v);
                }
            });
        }
        if (preset === 'apps'){
            $.each(all_rows, function(i,v){
                if ($(v).children('.type_col').text() === 'App'){
                    table_instance.fnSelect(v);
                }
            });
        }
        if (preset === 'dlc'){
            $.each(all_rows, function(i,v){
                if ($(v).children('.type_col').text() === 'DLC'){
                    table_instance.fnSelect(v);
                }
            });
        }
        if (preset === 'movies'){
            $.each(all_rows, function(i,v){
                if ($(v).children('.type_col').text() === 'Movie'){
                    table_instance.fnSelect(v);
                }
            });
        }
        if (preset === 'mac'){
            $.each(all_rows, function(i,v){
                if ($(v).find('.os_mac_col i span').text() === '1'){
                    table_instance.fnSelect(v);
                }
            });
        }
        if (preset === 'linux'){
            $.each(all_rows, function(i,v){
                if ($(v).find('.os_linux_col i span').text() === '1'){
                    table_instance.fnSelect(v);
                }
            });
        }
        if (preset === 'windows'){
            $.each(all_rows, function(i,v){
                if ($(v).find('.os_windows_col i span').text() === '1'){
                    table_instance.fnSelect(v);
                }
            });
        }
        if (preset === 'multiplayer'){
            $.each(all_rows, function(i,v){
                if (($(v).find('.multiplayer_col .icon-ok').length > 0)){
                    table_instance.fnSelect(v);
                }
            });
        }
        if (preset === 'controller'){
            $.each(all_rows, function(i,v){
                if (($(v).children('.controller_support_col').text() === 'partial') || ($(v).children('.controller_support_col').text() === 'full')){
                    table_instance.fnSelect(v);
                }
            });
        }
    }

    function sortNumber(a,b){
        return a-b;
    }

    var tableToExcel = (function() {
        var uri = 'data:application/vnd.ms-excel;base64,',
            template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--><meta http-equiv="content-type" content="text/plain; charset=UTF-8"/></head><body><table>{table}</table></body></html>',
            base64 = function(s) {
                return window.btoa(unescape(encodeURIComponent(s)));
            }, format = function(s, c) {
                return s.replace(/{(\w+)}/g, function(m, p) {
                    return c[p];
                });
            };
        return function(table, name) {
            if (!table.nodeType) table = document.getElementById(table);
            var ctx = {
                worksheet: name || 'Worksheet',
                table: table.innerHTML
            };
            window.location.href = uri + base64(format(template, ctx));
        };
    })();
