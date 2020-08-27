package com.stacksimplify.restservices.configuration;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.databind.annotation.JsonTypeIdResolver;
import com.fasterxml.jackson.databind.jsontype.impl.TypeIdResolverBase;
import org.hibernate.validator.internal.engine.path.PathImpl;
import org.springframework.http.HttpStatus;
import org.springframework.validation.FieldError;
import org.springframework.validation.ObjectError;

import javax.validation.ConstraintViolation;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

@JsonTypeInfo(include = JsonTypeInfo.As.WRAPPER_OBJECT, use = JsonTypeInfo.Id.CUSTOM, property = "error", visible = true)
@JsonTypeIdResolver(LowerCaseClassNameResolver.class)
class ApiError {

	private HttpStatus status;
	@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "dd-MM-yyyy hh:mm:ss")
	private LocalDateTime timestamp;
	private String message;
	private String debugMessage;
	private List<ApiSubError> subErrors;

	public ApiError(HttpStatus status, LocalDateTime timestamp, String message, String debugMessage,
			List<ApiSubError> subErrors) {
		super();
		this.status = status;
		this.timestamp = timestamp;
		this.message = message;
		this.debugMessage = debugMessage;
		this.subErrors = subErrors;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((debugMessage == null) ? 0 : debugMessage.hashCode());
		result = prime * result + ((message == null) ? 0 : message.hashCode());
		result = prime * result + ((status == null) ? 0 : status.hashCode());
		result = prime * result + ((subErrors == null) ? 0 : subErrors.hashCode());
		result = prime * result + ((timestamp == null) ? 0 : timestamp.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		ApiError other = (ApiError) obj;
		if (debugMessage == null) {
			if (other.debugMessage != null)
				return false;
		} else if (!debugMessage.equals(other.debugMessage))
			return false;
		if (message == null) {
			if (other.message != null)
				return false;
		} else if (!message.equals(other.message))
			return false;
		if (status != other.status)
			return false;
		if (subErrors == null) {
			if (other.subErrors != null)
				return false;
		} else if (!subErrors.equals(other.subErrors))
			return false;
		if (timestamp == null) {
			if (other.timestamp != null)
				return false;
		} else if (!timestamp.equals(other.timestamp))
			return false;
		return true;
	}

	public HttpStatus getStatus() {
		return status;
	}

	public void setStatus(HttpStatus status) {
		this.status = status;
	}

	public LocalDateTime getTimestamp() {
		return timestamp;
	}

	public void setTimestamp(LocalDateTime timestamp) {
		this.timestamp = timestamp;
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}

	public String getDebugMessage() {
		return debugMessage;
	}

	public void setDebugMessage(String debugMessage) {
		this.debugMessage = debugMessage;
	}

	public List<ApiSubError> getSubErrors() {
		return subErrors;
	}

	public void setSubErrors(List<ApiSubError> subErrors) {
		this.subErrors = subErrors;
	}

	private ApiError() {
		timestamp = LocalDateTime.now();
	}

	ApiError(HttpStatus status) {
		this();
		this.status = status;
	}

	ApiError(HttpStatus status, Throwable ex) {
		this();
		this.status = status;
		this.message = "Unexpected error";
		this.debugMessage = ex.getLocalizedMessage();
	}

	ApiError(HttpStatus status, String message, Throwable ex) {
		this();
		this.status = status;
		this.message = message;
		this.debugMessage = ex.getLocalizedMessage();
	}

	private void addSubError(ApiSubError subError) {
		if (subErrors == null) {
			subErrors = new ArrayList<>();
		}
		subErrors.add(subError);
	}

	private void addValidationError(String object, String field, Object rejectedValue, String message) {
		addSubError(new ApiValidationError(object, field, rejectedValue, message));
	}

	private void addValidationError(String object, String message) {
		addSubError(new ApiValidationError(object, message));
	}

	private void addValidationError(FieldError fieldError) {
		this.addValidationError(fieldError.getObjectName(), fieldError.getField(), fieldError.getRejectedValue(),
				fieldError.getDefaultMessage());
	}

	void addValidationErrors(List<FieldError> fieldErrors) {
		fieldErrors.forEach(this::addValidationError);
	}

	private void addValidationError(ObjectError objectError) {
		this.addValidationError(objectError.getObjectName(), objectError.getDefaultMessage());
	}

	void addValidationError(List<ObjectError> globalErrors) {
		globalErrors.forEach(this::addValidationError);
	}

	/**
	 * Utility method for adding error of ConstraintViolation. Usually when
	 * a @Validated validation fails.
	 *
	 * @param cv the ConstraintViolation
	 */
	private void addValidationError(ConstraintViolation<?> cv) {
		this.addValidationError(cv.getRootBeanClass().getSimpleName(),
				((PathImpl) cv.getPropertyPath()).getLeafNode().asString(), cv.getInvalidValue(), cv.getMessage());
	}

	void addValidationErrors(Set<ConstraintViolation<?>> constraintViolations) {
		constraintViolations.forEach(this::addValidationError);
	}

	abstract class ApiSubError {

	}

	class ApiValidationError extends ApiSubError {
		private String object;
		private String field;
		private Object rejectedValue;
		private String message;

		public ApiValidationError(String object, String field, Object rejectedValue, String message) {
			super();
			this.object = object;
			this.field = field;
			this.rejectedValue = rejectedValue;
			this.message = message;
		}

		ApiValidationError(String object, String message) {
			this.object = object;
			this.message = message;
		}

		public String getObject() {
			return object;
		}

		public void setObject(String object) {
			this.object = object;
		}

		public String getField() {
			return field;
		}

		public void setField(String field) {
			this.field = field;
		}

		public Object getRejectedValue() {
			return rejectedValue;
		}

		public void setRejectedValue(Object rejectedValue) {
			this.rejectedValue = rejectedValue;
		}

		public String getMessage() {
			return message;
		}

		public void setMessage(String message) {
			this.message = message;
		}

		@Override
		public int hashCode() {
			final int prime = 31;
			int result = 1;
			result = prime * result + getEnclosingInstance().hashCode();
			result = prime * result + ((field == null) ? 0 : field.hashCode());
			result = prime * result + ((message == null) ? 0 : message.hashCode());
			result = prime * result + ((object == null) ? 0 : object.hashCode());
			result = prime * result + ((rejectedValue == null) ? 0 : rejectedValue.hashCode());
			return result;
		}

		@Override
		public boolean equals(Object obj) {
			if (this == obj)
				return true;
			if (obj == null)
				return false;
			if (getClass() != obj.getClass())
				return false;
			ApiValidationError other = (ApiValidationError) obj;
			if (!getEnclosingInstance().equals(other.getEnclosingInstance()))
				return false;
			if (field == null) {
				if (other.field != null)
					return false;
			} else if (!field.equals(other.field))
				return false;
			if (message == null) {
				if (other.message != null)
					return false;
			} else if (!message.equals(other.message))
				return false;
			if (object == null) {
				if (other.object != null)
					return false;
			} else if (!object.equals(other.object))
				return false;
			if (rejectedValue == null) {
				if (other.rejectedValue != null)
					return false;
			} else if (!rejectedValue.equals(other.rejectedValue))
				return false;
			return true;
		}

		private ApiError getEnclosingInstance() {
			return ApiError.this;
		}
	}
}

class LowerCaseClassNameResolver extends TypeIdResolverBase {

	@Override
	public String idFromValue(Object value) {
		return value.getClass().getSimpleName().toLowerCase();
	}

	@Override
	public String idFromValueAndType(Object value, Class<?> suggestedType) {
		return idFromValue(value);
	}

	@Override
	public JsonTypeInfo.Id getMechanism() {
		return JsonTypeInfo.Id.CUSTOM;
	}
}