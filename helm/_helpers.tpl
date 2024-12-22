{{- define "stack-ai-vector-db.service.ports" -}}
ports:
  - name: tcp
    targetPort: tcp
    port: {{ .Values.vector-db.port }}
{{- end -}}
