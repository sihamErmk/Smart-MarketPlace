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

        // Injection des dépendances : logger pour les logs, service IQwen pour la génération des missions
        public JobMissionController(ILogger<JobMissionController> logger, IQwenService qwenService)
        {
            _logger = logger;
            _qwenService = qwenService;
        }

        // Point d'entrée POST pour générer une mission à partir d'une requête JSON
        [HttpPost("generate")]
        public async Task<IActionResult> GenerateMission([FromBody] JobMissionRequest request)
        {
            // Log de la réception de la requête avec le prompt reçu
            _logger.LogInformation($"Received mission generation request with prompt: {request?.Prompt}");
            
            // Vérification que la requête et le prompt ne sont pas vides
            if (request == null || string.IsNullOrEmpty(request.Prompt))
            {
                _logger.LogWarning("Empty prompt received");
                // Retourne une erreur 400 Bad Request avec un message d'erreur
                return BadRequest(new { error = "Prompt cannot be empty" });
            }

            // Appel asynchrone au service IQwen pour générer la mission, langue par défaut = anglais
            var result = await _qwenService.GenerateMissionAsync(request.Prompt, request.Language ?? "english");
            
            // Vérification si la réponse est une erreur, dans ce cas on log l'erreur et on retourne une BadRequest
            if (result is ErrorResponse errorResponse)
            {
                _logger.LogError($"Error generating mission: {errorResponse.Error}");
                return BadRequest(errorResponse);
            }
            
            // Succès : log d'information et retourne le résultat avec un code 200 OK
            _logger.LogInformation("Successfully generated mission");
            return Ok(result);
        }
    }
}
