using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using SmartMarketPlace.API.Services;
using SmartMarketPlace.Models;

namespace SmartMarketPlace.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class JobMissionController : ControllerBase
    {
        private readonly ILogger<JobMissionController> _logger;
        private readonly IQwenService _qwenService;

        public JobMissionController(ILogger<JobMissionController> logger, IQwenService qwenService)
        {
            _logger = logger;
            _qwenService = qwenService;
        }

        [HttpPost("generate")]
        public async Task<IActionResult> GenerateMission([FromBody] JobMissionRequest request)
        {
            _logger.LogInformation($"Received mission generation request with prompt: {request?.Prompt}");
            
            if (request == null || string.IsNullOrEmpty(request.Prompt))
            {
                _logger.LogWarning("Empty prompt received");
                return BadRequest(new { error = "Prompt cannot be empty" });
            }

            var result = await _qwenService.GenerateMissionAsync(request.Prompt, request.Language ?? "english");
            
            if (result is ErrorResponse errorResponse)
            {
                _logger.LogError($"Error generating mission: {errorResponse.Error}");
                return BadRequest(errorResponse);
            }
            
            _logger.LogInformation("Successfully generated mission");
            return Ok(result);
        }
    }
}