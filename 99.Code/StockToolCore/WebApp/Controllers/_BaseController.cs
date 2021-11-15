using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using System;

namespace WebApp.Controllers
{
    [FilterResult]
    public class _BaseController : ControllerBase { }

    public class FilterResult : Attribute, IResultFilter
    {
        public void OnResultExecuted(ResultExecutedContext context) { }
        public void OnResultExecuting(ResultExecutingContext context)
        {
            context.HttpContext.Response.Headers.Add("Access-Control-Allow-Origin", "*");
        }
    }
}
