package com.stacksimplify.restservices.configuration;

import java.util.NoSuchElementException;

import org.hibernate.exception.ConstraintViolationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.ServletWebRequest;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.web.servlet.NoHandlerFoundException;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

@Order(Ordered.HIGHEST_PRECEDENCE)
@ControllerAdvice
public class RestExceptionHandler extends ResponseEntityExceptionHandler {

	private static final Logger logger = LoggerFactory.getLogger(RestExceptionHandler.class);

	@ExceptionHandler(javax.validation.ConstraintViolationException.class)
	protected ResponseEntity<Object> handleConstraintViolation(javax.validation.ConstraintViolationException ex) {
		logger.error("Constraint Voilation Exception, ", ex);
		ApiError apiError = new ApiError(HttpStatus.BAD_REQUEST);
		apiError.setMessage("Validation error");
		apiError.addValidationErrors(ex.getConstraintViolations());
		return buildResponseEntity(apiError);
	}
	
	@Override
	protected ResponseEntity<Object> handleMethodArgumentNotValid(MethodArgumentNotValidException ex,
			HttpHeaders headers, HttpStatus status, WebRequest request) {
		logger.error("Method Argument Not Valid Exception, ", ex);
		ApiError apiError = new ApiError(HttpStatus.BAD_REQUEST);
		apiError.setMessage("Validation error");
		apiError.addValidationErrors(ex.getBindingResult().getFieldErrors());
		apiError.addValidationError(ex.getBindingResult().getGlobalErrors());
		return buildResponseEntity(apiError);
	}


	@ExceptionHandler(RecordNotFoundException.class)
	protected ResponseEntity<Object> handleEntityNotFound(RecordNotFoundException ex, WebRequest request) {
		logger.error("Entity Not Found Exception, ", ex);

		String acceptHeaderValue = request.getHeader("Accept");
		if (acceptHeaderValue == null || acceptHeaderValue.trim().isEmpty()) {
			acceptHeaderValue = "";
		}

		if (acceptHeaderValue.contains(MediaType.TEXT_XML_VALUE)
				|| acceptHeaderValue.contains(MediaType.TEXT_HTML_VALUE)
				|| acceptHeaderValue.contains(MediaType.APPLICATION_XHTML_XML_VALUE)
				|| acceptHeaderValue.contains(MediaType.APPLICATION_XML_VALUE)) {

			ServletUriComponentsBuilder builder = ServletUriComponentsBuilder.fromCurrentContextPath();
			builder.path("/error404.html");
			builder.build().toUri();

			HttpHeaders headers = new HttpHeaders();
			headers.setLocation(builder.build().toUri());
			return new ResponseEntity<>(headers, HttpStatus.NOT_FOUND);
		} else {
			ApiError apiError = new ApiError(HttpStatus.NOT_FOUND);
			apiError.setMessage("Resource not found!");
			apiError.setDebugMessage(ex.getMessage());
			return buildResponseEntity(apiError);
		}
	}

	@ExceptionHandler(NoSuchElementException.class)
	protected ResponseEntity<Object> handleNoSuchElementException(NoSuchElementException ex, WebRequest request) {
		logger.error("No Such Element Exception, ", ex);

		String acceptHeaderValue = request.getHeader("Accept");
		if (acceptHeaderValue == null || acceptHeaderValue.trim().isEmpty()) {
			acceptHeaderValue = "";
		}

		if (acceptHeaderValue.contains(MediaType.TEXT_XML_VALUE)
				|| acceptHeaderValue.contains(MediaType.TEXT_HTML_VALUE)
				|| acceptHeaderValue.contains(MediaType.APPLICATION_XHTML_XML_VALUE)
				|| acceptHeaderValue.contains(MediaType.APPLICATION_XML_VALUE)) {

			ServletUriComponentsBuilder builder = ServletUriComponentsBuilder.fromCurrentContextPath();
			builder.path("/error404.html");
			builder.build().toUri();

			HttpHeaders headers = new HttpHeaders();
			headers.setLocation(builder.build().toUri());
			return new ResponseEntity<>(headers, HttpStatus.NOT_FOUND);
		} else {
			ApiError apiError = new ApiError(HttpStatus.NOT_FOUND);
			apiError.setMessage("Resource not found!");
			apiError.setDebugMessage(ex.getMessage());
			return buildResponseEntity(apiError);
		}
	}

	@ExceptionHandler(javax.persistence.EntityNotFoundException.class)
	protected ResponseEntity<Object> handleEntityNotFound(javax.persistence.EntityNotFoundException ex,
			WebRequest request) {
		logger.error("Entity Not Found Exception, ", ex);
		String acceptHeaderValue = request.getHeader("Accept");
		if (acceptHeaderValue == null || acceptHeaderValue.trim().isEmpty()) {
			acceptHeaderValue = "";
		}

		if (acceptHeaderValue.contains(MediaType.TEXT_XML_VALUE)
				|| acceptHeaderValue.contains(MediaType.TEXT_HTML_VALUE)
				|| acceptHeaderValue.contains(MediaType.APPLICATION_XHTML_XML_VALUE)
				|| acceptHeaderValue.contains(MediaType.APPLICATION_XML_VALUE)) {

			ServletUriComponentsBuilder builder = ServletUriComponentsBuilder.fromCurrentContextPath();
			builder.path("/error404.html");
			builder.build().toUri();

			HttpHeaders headers = new HttpHeaders();
			headers.setLocation(builder.build().toUri());
			return new ResponseEntity<>(headers, HttpStatus.NOT_FOUND);
		} else {
			ApiError apiError = new ApiError(HttpStatus.NOT_FOUND);
			apiError.setMessage("Resource not found!");
			apiError.setDebugMessage(ex.getMessage());
			return buildResponseEntity(apiError);
		}
	}

	@Override
	protected ResponseEntity<Object> handleHttpMessageNotReadable(HttpMessageNotReadableException ex,
			HttpHeaders headers, HttpStatus status, WebRequest request) {
		logger.error("Http Message Not Readable Exception, ", ex);
		ServletWebRequest servletWebRequest = (ServletWebRequest) request;
		// log.info("{} to {}", servletWebRequest.getHttpMethod(),
		// servletWebRequest.getRequest().getServletPath());
		String error = "Malformed JSON request";
		return buildResponseEntity(new ApiError(HttpStatus.BAD_REQUEST, error, ex));
	}

	@Override
	protected ResponseEntity<Object> handleNoHandlerFoundException(NoHandlerFoundException ex, HttpHeaders headers,
			HttpStatus status, WebRequest request) {
		logger.error("No Handler Found Exception, ", ex);
		ApiError apiError = new ApiError(HttpStatus.BAD_REQUEST);
		apiError.setMessage(
				String.format("Could not find the %s method for URL %s", ex.getHttpMethod(), ex.getRequestURL()));
		apiError.setDebugMessage(ex.getMessage());
		return buildResponseEntity(apiError);
	}

	@ExceptionHandler(DataIntegrityViolationException.class)
	protected ResponseEntity<Object> handleDataIntegrityViolation(DataIntegrityViolationException ex,
			WebRequest request) {
		logger.error("Data Integrity Voilation Exception, ", ex);
		if (ex.getCause() instanceof ConstraintViolationException) {
			return buildResponseEntity(new ApiError(HttpStatus.CONFLICT, "Database error", ex.getCause()));
		}
		return buildResponseEntity(new ApiError(HttpStatus.INTERNAL_SERVER_ERROR, ex));
	}

	@ExceptionHandler(ResponseStatusException.class)
	protected ResponseEntity<Object> handleResponseStatusException(ResponseStatusException ex, WebRequest request) {
		logger.error("Response Status Exception, ", ex);
		ApiError apiError = new ApiError(ex.getStatus());
		apiError.setMessage(ex.getReason());
		apiError.setDebugMessage(ex.getMessage());
		return buildResponseEntity(apiError);
	}

	@ExceptionHandler(AccessDeniedException.class)
	protected ResponseEntity<Object> handleAccessDeniedException(AccessDeniedException ex, WebRequest request) {
		logger.error("Access Denied Exception, ", ex);
		String acceptHeaderValue = request.getHeader("Accept");
		if (acceptHeaderValue == null || acceptHeaderValue.trim().isEmpty()) {
			acceptHeaderValue = "";
		}

		if (acceptHeaderValue.contains(MediaType.TEXT_XML_VALUE)
				|| acceptHeaderValue.contains(MediaType.TEXT_HTML_VALUE)
				|| acceptHeaderValue.contains(MediaType.APPLICATION_XHTML_XML_VALUE)
				|| acceptHeaderValue.contains(MediaType.APPLICATION_XML_VALUE)) {

			ServletUriComponentsBuilder builder = ServletUriComponentsBuilder.fromCurrentContextPath();
			builder.path("/error403.html");
			builder.build().toUri();

			HttpHeaders headers = new HttpHeaders();
			headers.setLocation(builder.build().toUri());
			return new ResponseEntity<>(headers, HttpStatus.FORBIDDEN);
		} else {
			ApiError apiError = new ApiError(HttpStatus.FORBIDDEN);
			apiError.setMessage(
					"Access denied. If you think you should have access to this resource, please contact stacksimplify support.");
			apiError.setDebugMessage(ex.getMessage());
			return buildResponseEntity(apiError);
		}
	}

	@ExceptionHandler(Exception.class)
	protected ResponseEntity<Object> handleGenericException(Exception ex, WebRequest request) {
		logger.error("Exception, ", ex);
		String acceptHeaderValue = request.getHeader("Accept");
		if (acceptHeaderValue == null || acceptHeaderValue.trim().isEmpty()) {
			acceptHeaderValue = "";
		}

		if (acceptHeaderValue.contains(MediaType.TEXT_XML_VALUE)
				|| acceptHeaderValue.contains(MediaType.TEXT_HTML_VALUE)
				|| acceptHeaderValue.contains(MediaType.APPLICATION_XHTML_XML_VALUE)
				|| acceptHeaderValue.contains(MediaType.APPLICATION_XML_VALUE)) {

			ServletUriComponentsBuilder builder = ServletUriComponentsBuilder.fromCurrentContextPath();
			builder.path("/error500.html");
			builder.build().toUri();

			HttpHeaders headers = new HttpHeaders();
			headers.setLocation(builder.build().toUri());
			return new ResponseEntity<>(headers, HttpStatus.INTERNAL_SERVER_ERROR);
		} else {
			ApiError apiError = new ApiError(HttpStatus.INTERNAL_SERVER_ERROR);
			apiError.setMessage(
					"Something went wrong, Please try again later! If the problem persists, please contact stacksimplify support.");
			apiError.setDebugMessage(ex.getMessage());
			return buildResponseEntity(apiError);
		}
	}

	private ResponseEntity<Object> buildResponseEntity(ApiError apiError) {
		return new ResponseEntity<>(apiError, apiError.getStatus());
	}

}