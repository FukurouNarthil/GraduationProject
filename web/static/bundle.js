(function (d3, topojson) {
  'use strict';

  const svg = d3.select('svg');

  const margin = { top: 0, right: 0, bottom: 0, left: 0 },
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

  const projection = d3.geoNaturalEarth1()
    .scale(280)
    .translate([width / 1.35, height / 1.3]);
  const pathGenerator = d3.geoPath().projection(projection);

  const g = svg.append('g');

  svg.call(d3.zoom().on('zoom', () => {
    g.attr('transform', d3.event.transform);
  }));

  Promise.all([
    d3.tsv('../static/50m.tsv'),
    d3.json('../static/50m.json')
  ]).then(([tsvData, topoJSONdata]) => {

    const countryName = tsvData.reduce((accumulator, d) => {
      accumulator[d.iso_n3] = d.name;
      return accumulator;
    }, {});

    /*
    const countryName = {};
    tsvData.forEach(d => {
      countryName[d.iso_n3] = d.name;
    });
    */

    const countries = topojson.feature(topoJSONdata, topoJSONdata.objects.countries);
    g.selectAll('path').data(countries.features)
      .enter().append('path')
      .attr('class', 'country')
      .attr('d', pathGenerator)
      .on('click', function (d) {
        console.log(countryName[d.id])
        $.ajax({
          url: '/',
          data: countryName[d.id],
          type: 'POST',
          success: function (response) {
            console.log(response)
            window.location.replace(response.redirect);
            console.log('succeed!')
          },
          error: function (error) {
            console.log(error);
          }
        })
      })
      .append('title')
      .text(d => countryName[d.id]);
  });

}(d3, topojson));

  //# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VzIjpbIi4uL2luZGV4LmpzIl0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7XG4gIHNlbGVjdCxcbiAganNvbixcbiAgdHN2LFxuICBnZW9QYXRoLFxuICBnZW9OYXR1cmFsRWFydGgxLFxuICB6b29tLFxuICBldmVudFxufSBmcm9tICdkMyc7XG5pbXBvcnQgeyBmZWF0dXJlIH0gZnJvbSAndG9wb2pzb24nO1xuXG5jb25zdCBzdmcgPSBzZWxlY3QoJ3N2ZycpO1xuXG5jb25zdCBwcm9qZWN0aW9uID0gZ2VvTmF0dXJhbEVhcnRoMSgpO1xuY29uc3QgcGF0aEdlbmVyYXRvciA9IGdlb1BhdGgoKS5wcm9qZWN0aW9uKHByb2plY3Rpb24pO1xuXG5jb25zdCBnID0gc3ZnLmFwcGVuZCgnZycpO1xuXG5nLmFwcGVuZCgncGF0aCcpXG4gICAgLmF0dHIoJ2NsYXNzJywgJ3NwaGVyZScpXG4gICAgLmF0dHIoJ2QnLCBwYXRoR2VuZXJhdG9yKHt0eXBlOiAnU3BoZXJlJ30pKTtcblxuc3ZnLmNhbGwoem9vbSgpLm9uKCd6b29tJywgKCkgPT4ge1xuICBnLmF0dHIoJ3RyYW5zZm9ybScsIGV2ZW50LnRyYW5zZm9ybSk7XG59KSk7XG5cblByb21pc2UuYWxsKFtcbiAgdHN2KCdodHRwczovL3VucGtnLmNvbS93b3JsZC1hdGxhc0AxLjEuNC93b3JsZC81MG0udHN2JyksXG4gIGpzb24oJ2h0dHBzOi8vdW5wa2cuY29tL3dvcmxkLWF0bGFzQDEuMS40L3dvcmxkLzUwbS5qc29uJylcbl0pLnRoZW4oKFt0c3ZEYXRhLCB0b3BvSlNPTmRhdGFdKSA9PiB7XG4gIFxuICBjb25zdCBjb3VudHJ5TmFtZSA9IHRzdkRhdGEucmVkdWNlKChhY2N1bXVsYXRvciwgZCkgPT4ge1xuICAgIGFjY3VtdWxhdG9yW2QuaXNvX24zXSA9IGQubmFtZTtcbiAgICByZXR1cm4gYWNjdW11bGF0b3I7XG4gIH0sIHt9KTtcbiAgXG4gIC8qXG4gIGNvbnN0IGNvdW50cnlOYW1lID0ge307XG4gIHRzdkRhdGEuZm9yRWFjaChkID0+IHtcbiAgICBjb3VudHJ5TmFtZVtkLmlzb19uM10gPSBkLm5hbWU7XG4gIH0pO1xuICAqL1xuICBcbiAgY29uc3QgY291bnRyaWVzID0gZmVhdHVyZSh0b3BvSlNPTmRhdGEsIHRvcG9KU09OZGF0YS5vYmplY3RzLmNvdW50cmllcyk7XG4gIGcuc2VsZWN0QWxsKCdwYXRoJykuZGF0YShjb3VudHJpZXMuZmVhdHVyZXMpXG4gICAgLmVudGVyKCkuYXBwZW5kKCdwYXRoJylcbiAgICAgIC5hdHRyKCdjbGFzcycsICdjb3VudHJ5JylcbiAgICAgIC5hdHRyKCdkJywgcGF0aEdlbmVyYXRvcilcbiAgICAuYXBwZW5kKCd0aXRsZScpXG4gICAgICAudGV4dChkID0+IGNvdW50cnlOYW1lW2QuaWRdKTtcbiAgXG59KTsiXSwibmFtZXMiOlsic2VsZWN0IiwiZ2VvTmF0dXJhbEVhcnRoMSIsImdlb1BhdGgiLCJ6b29tIiwiZXZlbnQiLCJ0c3YiLCJqc29uIiwiZmVhdHVyZSJdLCJtYXBwaW5ncyI6Ijs7O0VBV0EsTUFBTSxHQUFHLEdBQUdBLFNBQU0sQ0FBQyxLQUFLLENBQUMsQ0FBQzs7RUFFMUIsTUFBTSxVQUFVLEdBQUdDLG1CQUFnQixFQUFFLENBQUM7RUFDdEMsTUFBTSxhQUFhLEdBQUdDLFVBQU8sRUFBRSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsQ0FBQzs7RUFFdkQsTUFBTSxDQUFDLEdBQUcsR0FBRyxDQUFDLE1BQU0sQ0FBQyxHQUFHLENBQUMsQ0FBQzs7RUFFMUIsQ0FBQyxDQUFDLE1BQU0sQ0FBQyxNQUFNLENBQUM7T0FDWCxJQUFJLENBQUMsT0FBTyxFQUFFLFFBQVEsQ0FBQztPQUN2QixJQUFJLENBQUMsR0FBRyxFQUFFLGFBQWEsQ0FBQyxDQUFDLElBQUksRUFBRSxRQUFRLENBQUMsQ0FBQyxDQUFDLENBQUM7O0VBRWhELEdBQUcsQ0FBQyxJQUFJLENBQUNDLE9BQUksRUFBRSxDQUFDLEVBQUUsQ0FBQyxNQUFNLEVBQUUsTUFBTTtJQUMvQixDQUFDLENBQUMsSUFBSSxDQUFDLFdBQVcsRUFBRUMsUUFBSyxDQUFDLFNBQVMsQ0FBQyxDQUFDO0dBQ3RDLENBQUMsQ0FBQyxDQUFDOztFQUVKLE9BQU8sQ0FBQyxHQUFHLENBQUM7SUFDVkMsTUFBRyxDQUFDLG1EQUFtRCxDQUFDO0lBQ3hEQyxPQUFJLENBQUMsb0RBQW9ELENBQUM7R0FDM0QsQ0FBQyxDQUFDLElBQUksQ0FBQyxDQUFDLENBQUMsT0FBTyxFQUFFLFlBQVksQ0FBQyxLQUFLOztJQUVuQyxNQUFNLFdBQVcsR0FBRyxPQUFPLENBQUMsTUFBTSxDQUFDLENBQUMsV0FBVyxFQUFFLENBQUMsS0FBSztNQUNyRCxXQUFXLENBQUMsQ0FBQyxDQUFDLE1BQU0sQ0FBQyxHQUFHLENBQUMsQ0FBQyxJQUFJLENBQUM7TUFDL0IsT0FBTyxXQUFXLENBQUM7S0FDcEIsRUFBRSxFQUFFLENBQUMsQ0FBQzs7Ozs7Ozs7O0lBU1AsTUFBTSxTQUFTLEdBQUdDLGdCQUFPLENBQUMsWUFBWSxFQUFFLFlBQVksQ0FBQyxPQUFPLENBQUMsU0FBUyxDQUFDLENBQUM7SUFDeEUsQ0FBQyxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLFFBQVEsQ0FBQztPQUN6QyxLQUFLLEVBQUUsQ0FBQyxNQUFNLENBQUMsTUFBTSxDQUFDO1NBQ3BCLElBQUksQ0FBQyxPQUFPLEVBQUUsU0FBUyxDQUFDO1NBQ3hCLElBQUksQ0FBQyxHQUFHLEVBQUUsYUFBYSxDQUFDO09BQzFCLE1BQU0sQ0FBQyxPQUFPLENBQUM7U0FDYixJQUFJLENBQUMsQ0FBQyxJQUFJLFdBQVcsQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQzs7R0FFbkMsQ0FBQzs7OzsifQ==S