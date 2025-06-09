using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using SmartMarketPlace.Models;

namespace SmartMarketPlace.API.Services
{
    public interface IQwenService
    {
        Task<object> GenerateMissionAsync(string prompt, string language);
    }

    public class QwenService : IQwenService
    {
        private readonly ILogger<QwenService> _logger;
        private readonly string _pythonScriptPath;

        public QwenService(ILogger<QwenService> logger)
        {
            _logger = logger;
            
            // Get the absolute path to the Python script
            var baseDir = AppDomain.CurrentDomain.BaseDirectory;
            _pythonScriptPath = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "..", "..", "PythonScripts", "qwen_inference.py"));
            
            _logger.LogInformation($"Python script path: {_pythonScriptPath}");
            
            // Verify the script exists
            if (!File.Exists(_pythonScriptPath))
            {
                _logger.LogError($"Python script not found at: {_pythonScriptPath}");
            }
        }

        public async Task<object> GenerateMissionAsync(string prompt, string language)
        {
            try
            {
                _logger.LogInformation($"Generating mission for prompt: {prompt}, language: {language}");

                // Create process to run Python script
                var processInfo = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"\"{_pythonScriptPath}\" \"{prompt}\" \"{language}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                
                _logger.LogInformation($"Executing command: {processInfo.FileName} {processInfo.Arguments}");

                using var process = new Process { StartInfo = processInfo };
                var output = new StringBuilder();
                var error = new StringBuilder();

                process.OutputDataReceived += (sender, args) =>
                {
                    if (args.Data != null)
                    {
                        output.AppendLine(args.Data);
                    }
                };

                process.ErrorDataReceived += (sender, args) =>
                {
                    if (args.Data != null)
                    {
                        error.AppendLine(args.Data);
                        _logger.LogWarning($"Python stderr: {args.Data}");
                    }
                };

                process.Start();
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();
                await process.WaitForExitAsync();

                if (process.ExitCode != 0)
                {
                    _logger.LogError($"Python script error (exit code {process.ExitCode}): {error}");
                    return new ErrorResponse { Error = "Error executing Python script", RawResponse = error.ToString() };
                }

                var result = output.ToString().Trim();
                
                if (string.IsNullOrEmpty(result))
                {
                    _logger.LogError("Python script returned empty output");
                    return new ErrorResponse { Error = "Empty response from Python script" };
                }
                
                _logger.LogInformation($"Python script output length: {result.Length} characters");

                // Try to parse the result as JobMission
                try
                {
                    var options = new JsonSerializerOptions
                    {
                        PropertyNameCaseInsensitive = true
                    };
                    
                    var jobMission = JsonSerializer.Deserialize<JobMission>(result, options);
                    return jobMission;
                }
                catch (JsonException ex)
                {
                    _logger.LogError($"Error deserializing JSON: {ex.Message}");
                    _logger.LogError($"Raw output: {result}");
                    
                    // Try to parse as ErrorResponse
                    try
                    {
                        var errorResponse = JsonSerializer.Deserialize<ErrorResponse>(result);
                        return errorResponse;
                    }
                    catch
                    {
                        return new ErrorResponse { 
                            Error = "Invalid JSON response", 
                            RawResponse = result.Length > 1000 ? result.Substring(0, 1000) + "..." : result 
                        };
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Exception in GenerateMissionAsync: {ex}");
                return new ErrorResponse { Error = ex.Message };
            }
        }
    }
}