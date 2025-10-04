const map = document.getElementById('api-map');
  const legend = document.getElementById('api-legend');

  const colorMap = [
  { fill: '#fff', regions: [], min: 0, max: 1000000 },
  { fill: '#E8F5E9', regions: [], min: 1000000, max: 5000000 },
  { fill: '#A5D6A7', regions: [], min: 5000000, max: 10000000 },
  { fill: '#66BB6A', regions: [], min: 10000000, max: 20000000 },
  { fill: '#43A047', regions: [], min: 20000000, max: 50000000 },
  { fill: '#388E3C', regions: [], min: 50000000, max: 100000000 },
  { fill: '#2E7D32', regions: [], min: 100000000, max: 1000000000 },
  { fill: '#1B5E20', regions: [], min: 1000000000, max: 1 / 0 },
  ];

  const generateLegend = (colorMap) => {
  return colorMap
  .map(({ fill, min, max }) => {
  return `
  <li class="vector-map-legend__item my-2">
    <div class="vector-map-legend__color me-2 border" style="background-color: \$\{fill\}"></div>
    ${min} - ${max}
  </li>
  `;
  })
  .join('\n');
  };

  legend.innerHTML = generateLegend(colorMap);

  fetch('https://restcountries.eu/rest/v2/all')
  .then((response) => response.json())
  .then((data) => {
  data.map((country) => {
  const { alpha2Code, population, capital, flag } = country;
  const section = colorMap.find((section) => {
  return population >= section.min && population < section.max; }); if (!section) { return; }
    section.regions.push({ id: alpha2Code, tooltip: ` <div>
    <img src="${flag}" class="my-1" style="max-width: 40px">
</div>
`,
});
});

const mapInstance = new VectorMap(map, {
readonly: true,
strokeWidth: 0.2,
hover: false,
fill: 'white',
colorMap,
});
});