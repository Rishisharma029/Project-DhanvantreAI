param location string = 'eastus'
param environmentName string = 'auramed-env'
param containerAppName string = 'auramed-backend'
param containerImage string = 'auramedregistry.azurecr.io/backend:latest'

resource environment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: environmentName
  location: location
  properties: {}
}

resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: containerAppName
  location: location
  properties: {
    managedEnvironmentId: environment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
      }
    }
    template: {
      containers: [
        {
          name: containerAppName
          image: containerImage
          resources: {
            cpu: json('0.5')
            memory: '1.0Gi'
          }
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/live'
                port: 8000
              }
            }
            {
              type: 'Readiness'
              httpGet: {
                path: '/ready'
                port: 8000
              }
            }
          ]
        }
      ]
    }
  }
}
