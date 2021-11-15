using Microsoft.AspNetCore.Mvc;
using WebApp.Biz.StockAnalysis;

namespace WebApp.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class StockToolController : _BaseController
    {
        private readonly ILogger<StockToolController> _logger;

        public StockToolController(ILogger<StockToolController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IEnumerable<object> Get()
        {
            var rng = new Random();
            return Enumerable.Range(1, 5).Select(index => new
            {
                Date = DateTime.Now.AddDays(index),
                TemperatureC = rng.Next(-20, 55),
                Summary = ""
            })
            .ToArray();
        }

        [HttpGet, Route("GetK")]
        public IActionResult GetK(String code, Int32 period)
        {
            return Ok(new BizAPI().GetK(code, period));
        }

        [HttpGet, Route("GetStocks")]
        public IActionResult GetStocks()
        {
            return Ok(new BizAPI().GetStocks());
        }
    }
}
