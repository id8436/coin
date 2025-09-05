# 25.6.13
html="""
<table>
    <colgroup>
        <col width="44">
        <col width="*">
        <col width="84">
        <col width="84">
        <col width="84">
        <col width="84">
        <col width="94">
        <col width="84">
    </colgroup>
    <thead>
        <tr>
            <th class="lAlign">순위</th>
            <th class="lAlign">종목명</th>
            <th class="rAlign">현재가</th>
            <th class="rAlign">전일비</th>
            <th class="rAlign">
                <a href="javascript:void(0)" class="" data-field-name="changeRate">등락률 <i>-</i></a>
            </th>
            <th class="rAlign">
                <a href="javascript:void(0)" class="" data-field-name="marketCap">시가총액 <i>-</i></a>
            </th>
            <th class="rAlign">
                <a href="javascript:void(0)" class="" data-field-name="listedShareCount">상장주식수 <i>-</i></a>
            </th>
            <th class="rAlign last">
                <a href="javascript:void(0)" class="" data-field-name="foreignOwnRate">외국인 <i>-</i></a>
            </th>
        </tr>
    </thead>
    <tbody><tr class="first"><td class="first"><span class="time">1</span></td>
<td><a href="/quotes/A005930" class="txt">삼성전자</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">58,500</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>1,000</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-1.68%</span>
</td>
<td>
    <span class="num">
        3,454,109
    </span>
</td>
<td>
    <span class="num">
        5,919,637,922
    </span>
</td>
<td class="pR">
    <span class="num">
        49.82%
    </span>
</td>
</tr><tr><td class="first"><span class="time">2</span></td>
<td><a href="/quotes/A000660" class="txt">SK하이닉스</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">238,500</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>3,000</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+1.27%</span>
</td>
<td>
    <span class="num">
        1,723,546
    </span>
</td>
<td>
    <span class="num">
        728,002,365
    </span>
</td>
<td class="pR">
    <span class="num">
        55.19%
    </span>
</td>
</tr><tr><td class="first"><span class="time">3</span></td>
<td><a href="/quotes/A207940" class="txt">삼성바이오로직스</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">1,018,000</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>11,000</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-1.07%</span>
</td>
<td>
    <span class="num">
        722,416
    </span>
</td>
<td>
    <span class="num">
        71,174,000
    </span>
</td>
<td class="pR">
    <span class="num">
        12.92%
    </span>
</td>
</tr><tr><td class="first"><span class="time">4</span></td>
<td><a href="/quotes/A373220" class="txt">LG에너지솔루션</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">294,500</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>9,500</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-3.13%</span>
</td>
<td>
    <span class="num">
        689,130
    </span>
</td>
<td>
    <span class="num">
        234,000,000
    </span>
</td>
<td class="pR">
    <span class="num">
        4.06%
    </span>
</td>
</tr><tr class="last"><td class="first"><span class="time">5</span></td>
<td><a href="/quotes/A012450" class="txt">한화에어로스페이스</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">946,000</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>7,000</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-0.73%</span>
</td>
<td>
    <span class="num">
        444,584
    </span>
</td>
<td>
    <span class="num">
        47,296,201
    </span>
</td>
<td class="pR">
    <span class="num">
        45.73%
    </span>
</td>
</tr><tr class="line"><td class="first"><span class="time">6</span></td>
<td><a href="/quotes/A005380" class="txt">현대차</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">199,200</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>2,300</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-1.14%</span>
</td>
<td>
    <span class="num">
        406,035
    </span>
</td>
<td>
    <span class="num">
        204,757,766
    </span>
</td>
<td class="pR">
    <span class="num">
        36.01%
    </span>
</td>
</tr><tr><td class="first"><span class="time">7</span></td>
<td><a href="/quotes/A105560" class="txt">KB금융</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">105,900</span>
</td>
<td>
    <span class="num" data-realtime-change-price="yes"><i>-</i></span>
</td>
<td>
    <span class="num" data-realtime-change-ratio="yes">0.00%</span>
</td>
<td>
    <span class="num">
        403,205
    </span>
</td>
<td>
    <span class="num">
        381,462,103
    </span>
</td>
<td class="pR">
    <span class="num">
        78.16%
    </span>
</td>
</tr><tr><td class="first"><span class="time">8</span></td>
<td><a href="/quotes/A005935" class="txt">삼성전자우</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">48,000</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>800</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-1.64%</span>
</td>
<td>
    <span class="num">
        390,036
    </span>
</td>
<td>
    <span class="num">
        815,974,664
    </span>
</td>
<td class="pR">
    <span class="num">
        73.78%
    </span>
</td>
</tr><tr><td class="first"><span class="time">9</span></td>
<td><a href="/quotes/A000270" class="txt">기아</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">97,100</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>1,300</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-1.32%</span>
</td>
<td>
    <span class="num">
        384,947
    </span>
</td>
<td>
    <span class="num">
        397,672,632
    </span>
</td>
<td class="pR">
    <span class="num">
        38.79%
    </span>
</td>
</tr><tr class="last"><td class="first"><span class="time">10</span></td>
<td><a href="/quotes/A329180" class="txt">HD현대중공업</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">432,000</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>12,500</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+2.98%</span>
</td>
<td>
    <span class="num">
        377,730
    </span>
</td>
<td>
    <span class="num">
        88,773,116
    </span>
</td>
<td class="pR">
    <span class="num">
        10.74%
    </span>
</td>
</tr><tr class="line"><td class="first"><span class="time">11</span></td>
<td><a href="/quotes/A068270" class="txt">셀트리온</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">160,600</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>3,300</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-2.01%</span>
</td>
<td>
    <span class="num">
        356,771
    </span>
</td>
<td>
    <span class="num">
        222,425,958
    </span>
</td>
<td class="pR">
    <span class="num">
        21.44%
    </span>
</td>
</tr><tr><td class="first"><span class="time">12</span></td>
<td><a href="/quotes/A034020" class="txt">두산에너빌리티</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">54,650</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>50</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+0.09%</span>
</td>
<td>
    <span class="num">
        345,262
    </span>
</td>
<td>
    <span class="num">
        640,561,146
    </span>
</td>
<td class="pR">
    <span class="num">
        26.26%
    </span>
</td>
</tr><tr><td class="first"><span class="time">13</span></td>
<td><a href="/quotes/A035420" class="txt">NAVER</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">200,000</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>1,100</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+0.55%</span>
</td>
<td>
    <span class="num">
        315,448
    </span>
</td>
<td>
    <span class="num">
        158,437,008
    </span>
</td>
<td class="pR">
    <span class="num">
        48.56%
    </span>
</td>
</tr><tr><td class="first"><span class="time">14</span></td>
<td><a href="/quotes/A055550" class="txt">신한지주</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">59,300</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>700</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+1.19%</span>
</td>
<td>
    <span class="num">
        292,547
    </span>
</td>
<td>
    <span class="num">
        495,842,065
    </span>
</td>
<td class="pR">
    <span class="num">
        58.81%
    </span>
</td>
</tr><tr class="last"><td class="first"><span class="time">15</span></td>
<td><a href="/quotes/A028260" class="txt">삼성물산</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">167,200</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>900</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-0.54%</span>
</td>
<td>
    <span class="num">
        282,671
    </span>
</td>
<td>
    <span class="num">
        169,976,544
    </span>
</td>
<td class="pR">
    <span class="num">
        26.86%
    </span>
</td>
</tr><tr class="line"><td class="first"><span class="time">16</span></td>
<td><a href="/quotes/A012330" class="txt">현대모비스</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">282,500</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>2,000</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-0.70%</span>
</td>
<td>
    <span class="num">
        262,711
    </span>
</td>
<td>
    <span class="num">
        92,995,094
    </span>
</td>
<td class="pR">
    <span class="num">
        42.02%
    </span>
</td>
</tr><tr><td class="first"><span class="time">17</span></td>
<td><a href="/quotes/A042660" class="txt">한화오션</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">83,400</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>600</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-0.71%</span>
</td>
<td>
    <span class="num">
        251,565
    </span>
</td>
<td>
    <span class="num">
        306,413,394
    </span>
</td>
<td class="pR">
    <span class="num">
        12.70%
    </span>
</td>
</tr><tr><td class="first"><span class="time">18</span></td>
<td><a href="/quotes/A009540" class="txt">HD한국조선해양</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">353,500</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>13,000</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+3.82%</span>
</td>
<td>
    <span class="num">
        246,290
    </span>
</td>
<td>
    <span class="num">
        70,773,116
    </span>
</td>
<td class="pR">
    <span class="num">
        32.73%
    </span>
</td>
</tr><tr><td class="first"><span class="time">19</span></td>
<td><a href="/quotes/A032830" class="txt">삼성생명</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">125,800</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>3,200</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+2.61%</span>
</td>
<td>
    <span class="num">
        245,800
    </span>
</td>
<td>
    <span class="num">
        200,000,000
    </span>
</td>
<td class="pR">
    <span class="num">
        21.90%
    </span>
</td>
</tr><tr class="last"><td class="first"><span class="time">20</span></td>
<td><a href="/quotes/A011200" class="txt">HMM</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">23,400</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>400</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+1.74%</span>
</td>
<td>
    <span class="num">
        237,809
    </span>
</td>
<td>
    <span class="num">
        1,025,039,496
    </span>
</td>
<td class="pR">
    <span class="num">
        7.51%
    </span>
</td>
</tr><tr class="line"><td class="first"><span class="time">21</span></td>
<td><a href="/quotes/A035720" class="txt">카카오</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">51,800</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>1,300</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+2.57%</span>
</td>
<td>
    <span class="num">
        227,510
    </span>
</td>
<td>
    <span class="num">
        441,766,501
    </span>
</td>
<td class="pR">
    <span class="num">
        28.72%
    </span>
</td>
</tr><tr><td class="first"><span class="time">22</span></td>
<td><a href="/quotes/A086790" class="txt">하나금융지주</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">78,600</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>1,400</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+1.81%</span>
</td>
<td>
    <span class="num">
        223,224
    </span>
</td>
<td>
    <span class="num">
        284,723,889
    </span>
</td>
<td class="pR">
    <span class="num">
        67.56%
    </span>
</td>
</tr><tr><td class="first"><span class="time">23</span></td>
<td><a href="/quotes/A005490" class="txt">POSCO홀딩스</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">262,000</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>3,500</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-1.32%</span>
</td>
<td>
    <span class="num">
        211,235
    </span>
</td>
<td>
    <span class="num">
        80,932,952
    </span>
</td>
<td class="pR">
    <span class="num">
        29.22%
    </span>
</td>
</tr><tr><td class="first"><span class="time">24</span></td>
<td><a href="/quotes/A064350" class="txt">현대로템</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">186,000</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>6,300</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+3.51%</span>
</td>
<td>
    <span class="num">
        201,040
    </span>
</td>
<td>
    <span class="num">
        109,142,293
    </span>
</td>
<td class="pR">
    <span class="num">
        32.31%
    </span>
</td>
</tr><tr class="last"><td class="first"><span class="time">25</span></td>
<td><a href="/quotes/A138040" class="txt">메리츠금융지주</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">110,400</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>1,800</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-1.60%</span>
</td>
<td>
    <span class="num">
        198,556
    </span>
</td>
<td>
    <span class="num">
        180,014,473
    </span>
</td>
<td class="pR">
    <span class="num">
        16.03%
    </span>
</td>
</tr><tr class="line"><td class="first"><span class="time">26</span></td>
<td><a href="/quotes/A000810" class="txt">삼성화재</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">430,500</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>8,500</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-1.94%</span>
</td>
<td>
    <span class="num">
        196,238
    </span>
</td>
<td>
    <span class="num">
        46,011,155
    </span>
</td>
<td class="pR">
    <span class="num">
        55.94%
    </span>
</td>
</tr><tr><td class="first"><span class="time">27</span></td>
<td><a href="/quotes/A402340" class="txt">SK스퀘어</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">141,800</span>
</td>
<td>
    <span class="num up" data-realtime-change-price="yes"><i>▲</i>1,200</span>
</td>
<td>
    <span class="num up" data-realtime-change-ratio="yes">+0.85%</span>
</td>
<td>
    <span class="num">
        187,280
    </span>
</td>
<td>
    <span class="num">
        132,540,858
    </span>
</td>
<td class="pR">
    <span class="num">
        52.23%
    </span>
</td>
</tr><tr><td class="first"><span class="time">28</span></td>
<td><a href="/quotes/A015760" class="txt">한국전력</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">28,100</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>350</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-1.23%</span>
</td>
<td>
    <span class="num">
        180,071
    </span>
</td>
<td>
    <span class="num">
        641,964,077
    </span>
</td>
<td class="pR">
    <span class="num">
        19.45%
    </span>
</td>
</tr><tr><td class="first"><span class="time">29</span></td>
<td><a href="/quotes/A259960" class="txt">크래프톤</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">370,500</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>11,500</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-3.01%</span>
</td>
<td>
    <span class="num">
        176,760
    </span>
</td>
<td>
    <span class="num">
        47,388,676
    </span>
</td>
<td class="pR">
    <span class="num">
        42.92%
    </span>
</td>
</tr><tr class="last"><td class="first"><span class="time">30</span></td>
<td><a href="/quotes/A010130" class="txt">고려아연</a></td>
<td>
    <span class="num" data-realtime-trade-price="yes">776,000</span>
</td>
<td>
    <span class="num down" data-realtime-change-price="yes"><i>▼</i>7,000</span>
</td>
<td>
    <span class="num down" data-realtime-change-ratio="yes">-0.89%</span>
</td>
<td>
    <span class="num">
        160,657
    </span>
</td>
<td>
    <span class="num">
        20,703,283
    </span>
</td>
<td class="pR">
    <span class="num">
        12.08%
    </span>
</td>
</tr></tbody>
</table>"""